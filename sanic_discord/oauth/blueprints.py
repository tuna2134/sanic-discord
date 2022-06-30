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
            if state:
                if request.args.get("state"):
                    args = list(args)
                    args.insert(0, request.args.get("state"))
                else:
                    raise StateError("state is required.")
            return await func(
                request, await request.app.ctx.oauth2._exchange_code(request), *args, **kwargs
            )
        return wrapper
    return decorator