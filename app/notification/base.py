from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass