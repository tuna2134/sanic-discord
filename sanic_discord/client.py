from .http import HttpClient
from .config import Config

class Client:
    def __init__(self, config: Config):
        self.secret = config.secret
        self.id = config.id
        self.http = HttpClient(self)
