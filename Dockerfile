FROM python:3.12-slim AS builder

WORKDIR /app

ENV POETRY_VERSION=2.3.2 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main


FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

RUN adduser --disabled-password --gecos "" appuser

COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/openapi.json')"]

CMD ["uvicorn", "application:get_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
