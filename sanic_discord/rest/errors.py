class HttpException(Exception):
    """
    The base exception for all HTTP exceptions.
    """

class NotFoundException(HttpException):
    """
    If the request returns a 404."""