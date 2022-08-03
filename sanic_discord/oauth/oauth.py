"Oauth2 client for sanic."
from sanic import Sanic, Request, HTTPResponse

from typing import List, Optional, Tuple

from functools import wraps
from urllib import parse

from .errors import OauthException, StateError
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
        self.app.ctx.oauth2: Oauth2 = self

    async def close(self) -> None:
        """
        Closes the client.
        """
        await self.http.close()

    def exchange_code(self, state: bool = False):
        """
        Exchanges a code for an access token.

        Args:
            state (bool): If you use state in oauth url, you must do True.

        Raises:
            StateError: state is invalid.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
                results = (await self._exchange_code(request, state)) + args
                return await func(request, *results, **kwargs)
            return wrapper
        return decorator

    async def _exchange_code(self, request: Request, state: bool = False) -> Tuple[AccessToken, ...]:
        """
        Exchanges a code for an access token.

        Args:
            request (Request): The request.
            state (bool): If you use state in oauth url, you must do True.

        Raises:
            StateError: state is invalid.
        """
        args = []
        if state:
            if request.args.get("state"):
                args.append(request.args.get("state"))
            else:
                raise StateError("state is required.")
        code = request.args.get("code")
        if code is None:
            raise OauthException("code is invaild.")
        args.insert(0, AccessToken(await self.http.exchange_code(
            code, self.redirect_uri, self.client_id, self.client_secret
        ), self.http))
        return tuple(args)

    async def fetch_user(self, access_token: str) -> dict:
        """
        Fetches the user's profile using an access token.

        Args:
            access_token (str): The access token to use.

        Returns:
            dict: The user's profile.
        """
        return await self.http.fetch_user(access_token)
    
    async def fetch_guilds(self, access_token: str) -> List[dict]:
        return await self.http.fetch_guilds(access_token)

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

    def get_authorize_url(self, scope: List[str] = ["identify"], *, state: Optional[str] = None) -> str:
        """
        Generates a URL to authorize the application.

        Args:
            scope (Optional[List[str]]): The scope to request. Defaults to ["identify"].
            state (Optional[str]): The state to use. Defaults to None.

        Returns:
            str: The URL to authorize the application.
        """
        payload = {
            "client_id": self.client_id,
            "scope": ' '.join(scope),
            "response_type": "code",
            "redirect_uri": self.redirect_uri
        }
        if state is not None:
            payload["state"] = state
        return f"{self.http.BASEURL}/oauth2/authorize?" + parse.urlencode(payload)
