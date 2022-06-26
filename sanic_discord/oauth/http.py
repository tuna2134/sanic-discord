from httpx import AsyncClient

import asyncio

from .errors import NotFoundException, HttpException


class HttpClient:
    """
    Discord http client.
    
    Attributes:
        BASEURL (str): The base URL of the Discord API.
        client (httpx.AsyncClient): The client used to make requests."""
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
            r = await self.client.request(method, self.BASEURL + path, **kwargs)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 404:
                raise NotFoundException("Not found error")
            elif r.status_code == 429:
                await asyncio.sleep(r.headers["X-RateLimit-Reset-After"])
            elif r.status_code == 500:
                raise HttpException(r.json()["message"])

    def fetch_user(self, access_token: str) -> dict:
        """
        Fetches the user's profile using an access token.
        
        Args:
            access_token (str): The access token to use."""
        return self.request("GET", "/users/@me", headers={"Authorization": f"Bearer {access_token}"})

    def exchange_code(
        self, code: str, redirect_uri: str,
        client_id: int, client_secret: str
    ) -> dict:
        """
        Exchanges a code for an access token.

        Args:
            code (str): The code to exchange.
            redirect_uri (str): The redirect URI.
            client_id (int): The client ID.
            client_secret (str): The client secret.
        """
        return self.request("POST", "/oauth2/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def refresh_token(
        self, refresh_token: str, client_id: int, client_secret: str
    ) -> dict:
        """
        Refreshes an access token using a refresh token.

        Args:
            refresh_token (str): The refresh token to use.
        """
        return self.request("POST", "/oauth2/token", data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        }, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })