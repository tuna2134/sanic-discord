from sanic_discord.rest import RestClient

from typing import List


class HttpClient(RestClient):
    """
    Discord http client for oauth2.
    """

    def fetch_user(self, access_token: str) -> dict:
        """
        Fetches the user's profile using an access token.

        Args:
            access_token (str): The access token to use."""
        return self.request("GET", "/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    
    def fetch_guilds(self, access_token: str) -> List[dict]:
        return self.request("GET", "/users/@me/guilds", headers={"Authorization": f"Bearer {access_token}"})

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

    async def add_guild(
        self, guild_id: str, user_id: str, access_token: str
    ) -> None:
        await self.request(
            "GET", f"//guilds/{guild_id}/members/{user_id}",
            params={"access_token": access_token}
        )
