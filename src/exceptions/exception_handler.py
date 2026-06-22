import logging

from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse
from starlette.exceptions import HTTPException

from src.exceptions.exceptions import AppException

logger = logging.getLogger(__name__)


def _log_exception(
    request: Request,
    status_code: int,
    error_code: str,
    reason: str,
) -> None:
    log_message = (
        "exception status_code=%s error_code=%s reason=%s method=%s path=%s"
    )
    log_args = (status_code, error_code, reason, request.method, request.url.path)
    if status_code >= 500:
        logger.error(log_message, *log_args)
    else:
        logger.warning(log_message, *log_args)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    def app_exception_handler(request: Request, exc: AppException):
        _log_exception(request, exc.status_code, exc.error_code, exc.message)
        return UJSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "reason": exc.message,
                "request": str(request.url),
            },
        )

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        _log_exception(request, exc.status_code, exc.__class__.__name__, str(exc.detail))
        return UJSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "reason": exc.detail,
                "request": str(request.url),
            },
        )
