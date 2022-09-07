from .oauth import Oauth

frim sanic import Sanic
try:
    from sanic_jwt import initialize
    from sanic_jwt.exceptions import AuthenticationFailed
except ImportError:
    invalid = True
else:
    invalid = False

from typing import TypedDict


class OauthJWT(Oauth):

    def __init__(self, app: Sanic, options: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initialize()
