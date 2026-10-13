import logging
from time import perf_counter
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.logging_config import request_id_context


REQUEST_ID_HEADER = "X-Request-ID"

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER, str(uuid4()))
        token = request_id_context.set(request_id)
        request.state.request_id = request_id
        start = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (perf_counter() - start) * 1000
            logger.exception(
                f"request failed method={request.method} path={request.url.path} "
                f"duration_ms={duration_ms:.2f}"
            )
            raise
        else:
            duration_ms = (perf_counter() - start) * 1000
            logger.info(
                f"request completed method={request.method} path={request.url.path} "
                f"status_code={response.status_code} duration_ms={duration_ms:.2f}"
            )
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            request_id_context.reset(token)
