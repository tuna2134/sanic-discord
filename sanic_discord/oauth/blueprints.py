from sanic import Request, HTTPResponse

from functools import wraps

from .errors import StateError


def exchange_code(*args, **kwargs) -> callable:
    """
    Exchanges a code for an access token.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args_wrapper, **kwargs_wrapper) -> HTTPResponse:
            results = (await request.app.ctx.oauth2._exchange_code(request, *args, **kwargs)) + args_wrapper
            return await func(request, *results, **kwargs_wrapper)
        return wrapper
    return decorator