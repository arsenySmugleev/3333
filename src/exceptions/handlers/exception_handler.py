import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status
from starlette.exceptions import HTTPException

from src.exceptions.exceptions import AppException
from src.exceptions.schemas import ErrorResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=exc.error_code,
                reason=exc.message,
                request=str(request.url),
            ).model_dump(),
        )

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        status_code = exc.status_code
        error_code = exc.__class__.__name__
        reason = str(exc.detail)
        log_message = (
            "exception status_code=%s error_code=%s reason=%s method=%s path=%s"
        )
        log_args = (status_code, error_code, reason, request.method, request.url.path)
        if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
            logger.error(log_message, *log_args)
        else:
            logger.warning(log_message, *log_args)
        return JSONResponse(
            status_code=status_code,
            content=ErrorResponse(
                error=error_code,
                reason=reason,
                request=str(request.url),
            ).model_dump(),
        )
