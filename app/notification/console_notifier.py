from app.notification.base import BaseNotifier

class ConsoleNotifier(BaseNotifier):
    def notify(self, message):
        print(f"Notification: {message}")