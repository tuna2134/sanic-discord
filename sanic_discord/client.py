from .http import HttpClient
from functools import wraps
from .config import Config
from sanic.response import redirect

class Client:
    def __init__(self, config: Config):
        self.secret = config.secret
        self.id = config.id
        self.login_url = config.login_url
        self.callback_url = config.callback_url
        self.redirect_url = config.redirect_url
        self.http = HttpClient(self)
        
    async def callback(self, request):
        code = request.args.get("code")
        data = {
            "client_id": self.id,
            "client_secret": self.secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.callback_url
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = await self.http.request("/oauth2/token", data=data, headers=headers)
        res = redirect(self.redirect_url)
        res.cookies["token"] = data["access_token"]
        return res

    def oauth2_require(self):
        def decorator(f):
            @wraps(f)
            async def function(request, *args, **kwargs):
                token = request.cookies.get("token")
                if token is None:
                    return redirect(self.login_url)
                headers = {
                    "Authorization": "Bearer {}".format(token)
                }
                async with ClientSession() as session:
                    async with session.get("https://discord.com/api/v9/users/@me", headers=headers) as r:
                        data = await r.json()
                if data.get("id"):
                    return await f(request, data, *args, **kwargs)
                else:
                    return redirect(self.login_url)
            return function
        return decorator
