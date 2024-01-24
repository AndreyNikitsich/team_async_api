from typing import Any, Tuple


class ServiceError(Exception):
    """Base-class for clients that raise errors."""

    def __init__(
            self,
            message: str,
            status_code: int,
            body: Any,
            errors: Tuple[Exception, ...] = (),
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors
        self.body = body


class BadRequestError(ServiceError):
    """Exception representing a 400 status code."""
