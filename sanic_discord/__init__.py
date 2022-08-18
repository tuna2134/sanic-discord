"""
.. include:: ../README.md
"""
from .oauth import *
from .interaction import *

__version__ = "2.0.0"
__author__ = "tuna2134"
__all__ = (
    "Oauth2",
    "OauthException",
    "HttpException",
    "NotFoundException",
    "AccessToken",
    "AccessTokenType",
    "StateError",
    "exchange_code",

    "InteractionClient"
)
