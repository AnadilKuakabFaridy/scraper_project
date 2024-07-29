import re
import aiohttp
import aiofiles
import os
from bs4 import BeautifulSoup
from app.scraper.retry import retry
from app.storage.base import BaseStorage
from app.notification.base import BaseNotifier
from app.cache.redis_cache import RedisCache

class Scraper:
    def __init__(self, storage: BaseStorage, notifier: BaseNotifier, cache: RedisCache, page_limit: int = None, proxy: str = None):
        self.storage = storage
        self.notifier = notifier
        self.cache = cache
        self.page_limit = page_limit
        self.proxy = proxy
        self.base_url = "https://dentalstall.com/shop/"
        self.image_dir = "images"

    async def scrape(self):
        products = []
        page = 1
        updated_count = 0
        
        os.makedirs(self.image_dir, exist_ok=True)
        
        async with aiohttp.ClientSession() as session:
            while True:
                if self.page_limit and page > self.page_limit:
                    break
                
                url = f"{self.base_url}page/{page}/"
                html = await self._fetch_page(session, url)
                if not html:
                    break
                
                page_products = await self._parse_products(session, html)
                if not page_products:
                    break
                
                products.extend(page_products)
                updated_count += len(page_products)
                page += 1

        await self._save_products(products)
        self.notifier.notify(f"Scraped {len(products)} products, updated {updated_count} in DB")
        return updated_count

    @retry(retries=3, delay=5)
    async def _fetch_page(self, session, url):
        async with session.get(url, proxy=self.proxy) as response:
            if response.status == 200:
                return await response.text()
        return None

    async def _parse_products(self, session, html):
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        for product in soup.find_all('li', class_='product'):
            title = ""
            price = -1
            image_url = ""
            try:
                title = product.find('h2', class_='woo-loop-product__title').text.strip()
                price = product.find('span', class_='price')
                if not price:
                    price = product.find('span', class_='woocommerce-Price-amount')
                if price:
                    price = price.text.strip()
                    matches = re.findall(r'\u20b9(\d+(?:\.\d+)?)', price)
                    price = float(matches[-1])                
                else:
                    price = -1
                image_url = product.find('img', class_='attachment-woocommerce_thumbnail').get('data-lazy-src')
            except Exception as e:
                print(f"error is :{e}")
            cached_price = self.cache.get(title+"899")
            if cached_price is None or cached_price != price:
                self.cache.set(title, price)
                try:
                    image_path = await self._download_image(session, image_url, title)
                except Exception as e:
                    print(f"error in downloading image: {e}")
                    image_path = "N/A"
                products.append({
                    "product_title": title,
                    "product_price": price,
                    "path_to_image": image_path
                })
        
        return products

    async def _download_image(self, session, url, title):
        filename = f"{title.replace(' ', '_')}.jpg"
        filepath = os.path.join(self.image_dir, filename)
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)

        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(filepath, mode='wb') as f:
                    await f.write(await response.read())
                return filepath
        return None

    async def _save_products(self, products):
        await self.storage.save(products)