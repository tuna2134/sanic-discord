from .oauth import Oauth

frim sanic import Sanic
from sanic_jwt import initialize
from sanic_jwt.exceptions import AuthenticationFailed

from typing import TypedDict


class OauthJWT(Oauth):

    def __init__(self, app: Sanic, options: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initialize()
