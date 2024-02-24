import asyncio
import requests

class SungramBase:
    def __init__(self, token=None):
        """Initialize the SungramBase class with a Telegram API token."""
        self.token = token
        self.base_url = "https://api.telegram.org/bot"
        self.update_id = None

    def _make_request(self, method, params=None):
        """Make a request to the Telegram API."""
        url = f"{self.base_url}{self.token}/{method}"
        response = requests.post(url, data=params)
        return response.json()

    async def _poll_updates(self):
        """Continuously poll for updates using long polling."""
        while True:
            updates = self._make_request("getUpdates", params={"offset": self.update_id})
            for update in updates.get("result", []):
                self.handle_update(update)
                self.update_id = update["update_id"] + 1
            await asyncio.sleep(1)

    def handle_update(self, update):
        """Handle different types of updates."""
        # Placeholder for handling different types of updates
        pass

    def _start_event_loop(self):
        """Start the event loop for handling updates asynchronously."""
        loop = asyncio.get_event_loop()
        loop.create_task(self._poll_updates())
        loop.run_forever()

    def run(self):
        """Run the SungramBase client."""
        self._start_event_loop()
        
