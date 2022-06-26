from sanic.exceptions import SanicException


class OauthException(SanicException):
    status_code = 403

class HttpException(SanicException):
    status_code = 500

class NotFoundException(SanicException):
    status_code = 404