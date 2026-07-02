import logging
from typing import NoReturn

logger = logging.getLogger(__name__)


class AppException(Exception):
    status_code = 400
    error_code = "APP_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    status_code = 404
    error_code = "NOT_FOUND"


def raise_not_found(message: str) -> NoReturn:
    logger.warning("%s", message)
    raise NotFoundException(message)
