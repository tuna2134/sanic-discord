import aiohttp
from functools import wraps
from sanic.response import redirect
from .model import user

class ApiError(Exception):
    pass

class HttpClient:
    def __init__(self, token):
        self.token = token
        self.session = aiohttp.ClientSession()
        
    async def request(self, method, path, *args, **kwargs):
        headers = {
            "Authorization": f"Bot {self.token}"
        }
        if kwargs.get("json"):
            headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        for t in range(5):
            async with self.session.request(method, path, *args, **kwargs) as r:
                if r.status == 429:
                    data = await r.json()
                    if data["global"] is True:
                        raise ApiError("Now api is limit. Wait a minute please.")
                    else:
                        await sleep(data["retry_after"])
                else:
                    return await r.json()
                
    async def 
