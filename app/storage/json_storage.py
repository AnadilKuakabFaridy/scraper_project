import json
import aiofiles
from app.storage.base import BaseStorage

class JSONStorage(BaseStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    async def save(self, data):
        async with aiofiles.open(self.file_path, mode='w') as f:
            await f.write(json.dumps(data, indent=2))

    async def load(self):
        try:
            async with aiofiles.open(self.file_path, mode='r') as f:
                content = await f.read()
                return json.loads(content)
        except FileNotFoundError:
            return []
            