from sanic.exceptions import SanicException


class OauthException(SanicException):
    status_code = 403