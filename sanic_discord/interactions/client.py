from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from sanic import Sanic
from .http import HttpClient


class InteractionClient:
    def __init__(self, app: Sanic):
        self.app = app
