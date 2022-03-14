import aiohttp
from functools import wraps
from sanic.response import redirect

class ApiError(Exception):
    pass

class HttpClient:
    Baseurl = "https://discord.com/api/v9"
    def __init__(self):
        self.session = aiohttp.ClientSession()
        
    async def request(self, method, path, *args, **kwargs):
        for t in range(5):
            async with self.session.request(method, self.Baseurl + path, *args, **kwargs) as r:
                if r.status == 429:
                    data = await r.json()
                    if data["global"] is True:
                        raise ApiError("Now api is limit. Wait a minute please.")
                    else:
                        await sleep(data["retry_after"])
                else:
                    return await r.json()
