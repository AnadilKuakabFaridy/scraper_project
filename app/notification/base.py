from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        """
        Send a notification with the given message.
        
        :param message: The message to be sent in the notification
        """
        pass