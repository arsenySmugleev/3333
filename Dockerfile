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

ARG APP_UID=1000
ARG APP_GID=1000

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd --gid ${APP_GID} appuser \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --no-create-home --shell /usr/sbin/nologin appuser

COPY --from=builder /app/.venv /app/.venv
COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthcheck')"]

CMD ["uvicorn", "src.application:get_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
