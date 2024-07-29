from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional
from app.scraper.scraper import Scraper
from app.storage.json_storage import JSONStorage
from app.notification.console_notifier import ConsoleNotifier
from app.cache.redis_cache import RedisCache

app = FastAPI()
security = HTTPBearer()

class ScraperSettings(BaseModel):
    page_limit: Optional[int] = Field(None, description="Limit the number of pages to scrape")
    proxy: Optional[str] = Field(None, description="Proxy string to use for scraping")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your_static_token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials

@app.post("/scrape")
async def scrape_products(settings: ScraperSettings, token: str = Depends(verify_token)):
    storage = JSONStorage("products.json")
    notifier = ConsoleNotifier()
    cache = RedisCache()
    
    scraper = Scraper(
        storage=storage,
        notifier=notifier,
        cache=cache,
        page_limit=settings.page_limit
        # proxy=settings.proxy
    )
    
    result = await scraper.scrape()
    return {"message": "Scraping completed", "products_scraped": result}