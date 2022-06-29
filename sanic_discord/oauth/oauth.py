"Oauth2 client for sanic."
from sanic import Sanic, Request, HTTPResponse

from typing import List, Optional

from functools import wraps
from urllib import parse

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
        app (Sanic): The Sanic app.
        client_id (int): The client ID.
        client_secret (str): The client secret.
        redirect_uri (str): The redirect URI.
        client (httpx.AsyncClient): The client used to make requests.
    """
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
        """
        Exchanges a code for an access token.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
                code = request.args.get("code")
                if request.args.get("state"):
                    args.append(request.args.get("state"))
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

    def get_authorize_url(self, scope: Optional[List[str]] = None, *, state: Optional[str] = None) -> str:
        """
        Generates a URL to authorize the application.

        Args:
            scope (Optional[List[str]]): The scope to request. Defaults to ["identify"].

        Returns:
            str: The URL to authorize the application.
        """
        payload = {
            "client_id": self.client_id,
            "scope": ' '.join(scope) if scope is not None else 'identify',
            "response_type": "code",
            "redirect_uri": self.redirect_uri
        }
        if state is not None:
            payload["state"] = state
        print(parser.urlencode(payload))
        return f"{self.http.BASEURL}/oauth2/authorize" \
            f"?client_id={self.client_id}" \
            f"&scope={' '.join(scope) if scope is not None else 'identify'}" \
            f"&response_type=code&redirect_uri={self.redirect_uri}"
