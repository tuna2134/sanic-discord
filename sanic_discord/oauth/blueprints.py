from sanic import Request, HTTPResponse

from functools import wraps

from .errors import StateError


def exchange_code(state: bool = False) -> callable:
    """
    Exchanges a code for an access token.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
            results = (await request.app.ctx.oauth2._exchange_code(request, state)) + args
            return await func(request, *results, **kwargs)
        return wrapper
    return decorator