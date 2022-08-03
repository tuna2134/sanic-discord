from .http import HttpClient

from typing import TypedDict, List

from datetime import datetime, timedelta


class AccessTokenType(TypedDict):
    """
    The type of the access token."""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


class AccessToken:
    """
    Accesstoken object.

    Args:
        data (AccessTokenType): The access token data.
        http (HttpClient): The HTTP client to use.

    Attributes:
        access_token (str): The access token.
        token_type (str): The token type.
        refresh_token (str): The refresh token.
        scope (str): The scope.
        expires_in (datetime): The expiration date."""

    def __init__(self, data: AccessTokenType, http: HttpClient):
        self.http = http
        self.data = data
        self.access_token = data["access_token"]
        self.token_type = data["token_type"]
        self.refresh_token = data["refresh_token"]
        self.scope = data["scope"]
        self.expires_in = datetime.now(
        ) + timedelta(seconds=self.data["expires_in"])

    async def fetch_user(self) -> dict:
        """
        Fetches the user's profile using an access token.

        Returns:
            dict: The user's profile."""
        return await self.http.fetch_user(self.access_token)
    
    async def fetch_guilds(self) -> List[dict]:
        return await self.http.fetch_guilds(self.access_token)

    async def add_guild(self, guildid: int):
        pass
