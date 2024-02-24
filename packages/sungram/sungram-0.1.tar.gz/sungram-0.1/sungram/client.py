from .base import SungramBase

class SungramClient(SungramBase):
    def __init__(self, token):
        """Initialize the SungramClient with a Telegram user token."""
        super().__init__(token=token)

    def send_message(self, chat_id, text):
        """Send a message using the 'sendMessage' method of the Telegram API."""
        params = {"chat_id": chat_id, "text": text}
        self._make_request("sendMessage", params)
      
