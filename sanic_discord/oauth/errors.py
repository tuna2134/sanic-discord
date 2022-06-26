from sanic.exceptions import SanicException


class OauthException(SanicException):
    """
    The base exception for all Oauth2 exceptions.
    """
    status_code = 403

class HttpException(SanicException):
    """
    The base exception for all HTTP exceptions.
    """
    status_code = 500

class NotFoundException(HttpException):
    """
    If the request returns a 404."""
    status_code = 404