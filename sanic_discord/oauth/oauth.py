from httpx import AsyncClient
from sanic import Sanic, Request

from functools import wraps

from .errors import OauthException
from .access_token import AccessToken


class Oauth2:
    url: str = "https://discord.com/api/v10"
    def __init__(
        self, app: Sanic, client_id: int, client_secret: str, redirect_uri: str
    ):
        self.app = app
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client = AsyncClient()

    async def request(self, method: str, path: str, *args, **kwargs):
        return await self.client.request(method, self.url + path, **kwargs)

    def exchange_code(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                code = request.args.get("code")
                if code is None:
                    raise OauthException("No code provided")
                r = await self.request(
                    "POST",
                    "/oauth2/token", data={
                        "grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": self.redirect_uri,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret
                    }, headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                return await func(request, AccessToken(r.json()), *args, **kwargs)
            return wrapper
        return decorator

    async def refresh_token(self, refresh_token: str):
        r = await self.request(
            "POST",
            "/oauth2/token", data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }, headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        return AccessToken(r.json())