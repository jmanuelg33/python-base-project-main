from typing import Optional

class BaseAPIException(Exception):
    status_code = 500
    code = "UNKNOWN_ERROR"
    message = "internal server error"

    def __init__(self, code: Optional[str] = None, status_code: Optional[int] = None, message: Optional[str] = None):
        self.code = code or self.code
        self.status_code = status_code or self.status_code
        self.message = message or self.message

        super(BaseAPIException, self).__init__(self.message)

