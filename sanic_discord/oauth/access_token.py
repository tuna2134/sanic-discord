from typing import TypedDict

from datetime import datetime, timedelta


class AccessTokenType(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str

class AccessToken:
    def __init__(self, data: AccessTokenType):
        self.data = data
        self.access_token = data["access_token"]
        self.token_type = data["token_type"]
        self.refresh_token = data["refresh_token"]
        self.scope = data["scope"]

    @property
    def expires_in(self) -> datetime:
        return datetime.now() + timedelta(seconds=self.data["expires_in"])