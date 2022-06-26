from .http import HttpClient


class InteractionClient:
    """
    interaction client
    
    Args:
        token (str): The bot token.
        public_key (str): The public key.
        
    Attributes:
        http (HttpClient): The http client.
        token (str): The bot token.
        public_key (str): The public key."""
    def __init__(self, token: str, public_key: str):
        self.http = HttpClient()
        self.token = token
        self.public_key = public_key

    async def close(self) -> None:
        """
        Closes the client.
        """
        await self.http.close()