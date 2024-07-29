from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseStorage(ABC):
    @abstractmethod
    async def save(self, data: List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    async def load(self) -> List[Dict[str, Any]]:
        pass