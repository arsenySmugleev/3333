from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse
from starlette import status
from starlette.exceptions import HTTPException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    def not_found(request: Request, exc: HTTPException):
        return UJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": exc.__class__.__name__,
                "reason": exc.detail,
                "request": str(request.url)
            }
        )
