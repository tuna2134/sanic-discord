from sanic_discord.rest import RestClient


class HttpClient(RestClient):
    """
    Discord http client for interaction
    """
    def __init__(self, token: str, public_key: str):
        self.token = token
        self.public_key = public_key
        super().__init__()

    async def request(self, *args, **kwargs) -> dict:
        headers = {
            "Authorization": f"Bot {self.token}",
        }
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            kwargs["headers"] = headers
        else:
            kwargs["headers"] = headers
        return await super().request(*args, **kwargs)