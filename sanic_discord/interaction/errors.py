from sanic.exceptions import SanicException


class InteractionException(SanicException):
    """
    The base exception for all interaction exceptions.
    """
    status_code = 500

class InvaildSignatureError(InteractionException):
    """
    If the signature is invalid.
    """
    status_code = 401