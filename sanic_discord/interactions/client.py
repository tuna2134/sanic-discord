from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from sanic import Sanic, Request
from .http import HttpClient


class InteractionClient:
    def __init__(self, app: Sanic, *, public_key: str):
        self.app = app
        self.verifykey = VerifyKey(bytes.fromhex(publickey))
        
    async def interaction(self, request: Request):
        signature = request.headers.get("x-signature-ed25519")
        timestamp = request.headers.get("x-signature-timestamp")
        try:
            self.verify_key.verify(f'{timestamp}{request.body.decode()}'.encode(), bytes.fromhex(signature))
        except BadSignatureError:
            return text("invalid request signature", status=401)
        else:
            pass
