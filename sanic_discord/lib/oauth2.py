from aiohttp import ClientSession
from sanic.response import redirect
from functools import wraps

def require():
    def decorator(f):
        @wraps(f)
        async def function(request, *args, **kwargs):
            token = request.cookies.get("token")
            if token is None:
                return redirect("/login")
            headers = {
                "Authorization": "Bearer {}".format(token)
            }
            async with ClientSession() as session:
                async with session.get("https://discord.com/api/v9/users/@me", headers=headers) as r:
                    data = await r.json()
            if data.get("id"):
                return await f(request, data, *args, **kwargs)
            else:
                return redirect("/login")
        return function
    return decorator