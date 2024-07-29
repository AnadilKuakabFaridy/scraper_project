from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseStorage(ABC):
    @abstractmethod
    async def save(self, data: List[Dict[str, Any]]) -> None:
        """
        Save the given data to the storage.
        
        :param data: A list of dictionaries containing product information
        """
        pass

    @abstractmethod
    async def load(self) -> List[Dict[str, Any]]:
        """
        Load data from the storage.
        
        :return: A list of dictionaries containing product information
        """
        pass