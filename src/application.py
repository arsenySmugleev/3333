import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from starlette.middleware.cors import CORSMiddleware

from infrastructure.cache import RedisCache
from src.config import Settings
from src.controllers.v1.doctors import router as doctor_appointment
from src.controllers.v1.medical_cards import router as med_card_insurance
from src.controllers.v1.patients import router as patient_med_service
from src.exceptions.handlers.exception_handler import register_exception_handlers
from src.healthcheck.router import router as healthcheck_router
from src.logging_config import configure_logging
from src.request_id_middleware import RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    redis = Redis.from_url(str(settings.redis_url), decode_responses=True)
    cache = RedisCache(redis, settings.cache_ttl_seconds)

    app.state.redis = redis
    app.state.cache = cache

    yield

    await redis.aclose()


def get_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        docs_url="/docs",
        openapi_url="/openapi.json",
        default_response_class=JSONResponse,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)
    app.include_router(healthcheck_router)
    app.include_router(doctor_appointment, prefix="/api/v1")
    app.include_router(patient_med_service, prefix="/api/v1")
    app.include_router(med_card_insurance, prefix="/api/v1")

    register_exception_handlers(app)
    return app
