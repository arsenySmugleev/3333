import logging
import sys
from contextvars import ContextVar


DEFAULT_REQUEST_ID = "-"
request_id_context: ContextVar[str] = ContextVar("request_id", default=DEFAULT_REQUEST_ID)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


def configure_logging() -> None:
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s request_id=%(request_id)s "
            "%(name)s: %(message)s"
        )
    )

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    logging.getLogger("uvicorn.access").disabled = True
