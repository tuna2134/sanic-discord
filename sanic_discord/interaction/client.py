from sanic import Sanic, Request, HTTPResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from typing import List

from .http import HttpClient
from .errors import InvaildSignatureError


class InteractionClient:
    """
    interaction client
    
    Args:
        token (str): The bot token.
        public_key (str): The public key.
        
    Attributes:
        http (HttpClient): The http client.
        verify_key (nacl.signing.VerifyKey): The public key."""
    def __init__(self, app: Sanic, token: str, public_key: str):
        self.app = app
        self.http = HttpClient(token, public_key)
        self.verify_key = VerifyKey(bytes.fromhex(public_key))
        self.interaction_event: callable = None

    async def close(self) -> None:
        """
        Closes the client.
        """
        await self.http.close()

    def on_interaction(self, func: callable) -> callable:
        """
        Decorator for handling interaction requests.
        Interaction event cacher."""
        self.interaction_event = func
        return func

    async def handle_interaction(self, request: Request) -> HTTPResponse:
        """
        Handles an interaction request.
        """
        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        body = request.body.decode("utf-8")
        try:
            self.verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        except BadSignatureError:
            raise InvaildSignatureError("Invalid signature")
        else:
            return await self.interaction_event(request.json)