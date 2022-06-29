from httpx import AsyncClient

import asyncio

from .errors import NotFoundException, HttpException


class RestClient:
    """
    This is a base client for httpclient

    Attributes:
        client (httpx.AsyncClient): The client used to make requests.
        BASEURL (str): The base URL of the Discord API."""
    BASEURL = "https://discord.com/api/v10"

    def __init__(self):
        self.client = AsyncClient()

    async def close(self) -> None:
        """
        Closes the client."""
        await self.client.aclose()

    async def request(self, method: str, path: str, *args, **kwargs) -> dict:
        """
        Makes a request to the Discord API.
        Args:
            method (str): The HTTP method to use.
            path (str): The path to request.
            *args: Any additional arguments to pass to the request.
            **kwargs: Any additional keyword arguments to pass to the request.
        Raises:
            NotFoundException: If the request returns a 404.
            HttpException: If the request returns an error.
        Returns:
            httpx.Response: The response from the request."""
        for _ in range(10):
            r = await self.client.request(method, self.BASEURL + path, *args, **kwargs)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 404:
                raise NotFoundException("Not found error")
            elif r.status_code == 429:
                await asyncio.sleep(r.headers["X-RateLimit-Reset-After"])
            elif r.status_code == 500:
                raise HttpException(r.json()["message"])
