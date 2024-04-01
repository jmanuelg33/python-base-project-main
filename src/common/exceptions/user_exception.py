from src.common.exceptions import BaseAPIException
from src.common.constants import exceptions_codes


class EmailNotRegisteredException(BaseAPIException):
    status_code = 401
    code = exceptions_codes.EMAIL_NOT_REGISTERED


class InvalidCredentialsException(BaseAPIException):
    status_code = 403
    code = exceptions_codes.INVALID_CREDENTIALS


class JwtException(BaseAPIException):
    error_code = 403
    code = exceptions_codes.INVALID_AUTH_TOKEN
