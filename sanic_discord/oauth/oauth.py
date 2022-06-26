"Oauth2 client for sanic."
from sanic import Sanic, Request

from typing import List, Optional

from functools import wraps

from .errors import OauthException
from .access_token import AccessToken
from .http import HttpClient


class Oauth2:
    """
    The following methods are used to generate the URL to redirect to.
    
    Args:
        app (Sanic): The Sanic app.
        client_id (int): The client ID.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect URI.

    Attributes:
        url (str): The URL to the Discord API.
        app (Sanic): The Sanic app.
        client_id (int): The client ID.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect URI.
        client (httpx.AsyncClient): The client used to make requests.
    """
    url: str = "https://discord.com/api/v10"
    def __init__(
        self, app: Sanic, client_id: int, client_secret: str, redirect_uri: str
    ):
        self.app = app
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.http = HttpClient()

    async def close(self) -> None:
        """
        Closes the client.
        """
        await self.http.close()

    def exchange_code(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                code = request.args.get("code")
                if code is None:
                    raise OauthException("No code provided")
                return await func(request, AccessToken(
                    await self.http.exchange_code(
                        code, self.redirect_uri, self.client_id, self.client_secret
                    ), self.http), *args, **kwargs)
            return wrapper
        return decorator

    async def fetch_user(self, access_token: str) -> dict:
        """
        Fetches the user's profile using an access token.
        
        Args:
            access_token (str): The access token to use.
            
        Returns:
            dict: The user's profile.
        """
        return await self.http.fetch_user(access_token)

    async def refresh_token(self, refresh_token: str) -> AccessToken:
        """
        Refreshes an access token using a refresh token.

        Args:
            refresh_token (str): The refresh token to use.

        Returns:
            AccessToken: The new access token.
        """
        return AccessToken(await self.http.refresh_token(
            refresh_token, self.client_id, self.client_secret
        ), self.http)

    def get_authorize_url(self, scope: Optional[List[str]] = ["identify"]) -> str:
        """
        Generates a URL to authorize the application.

        Args:
            scope (List[str], optional): The scope to request. Defaults to ["identify"].

        Returns:
            str: The URL to authorize the application.
        """
        return f"{self.url}/oauth2/authorize" \
            f"?client_id={self.client_id}&scope={' '.join(scope)}" \
            f"&response_type=code&redirect_uri={self.redirect_uri}"