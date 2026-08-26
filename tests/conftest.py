import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer

from src.application import get_app
from src.db import get_session
from src.redis_client import RedisCache, get_cache
from src.services.doctor_appointment import DoctorAppointmentService
from src.services.med_card_insurance import MedCardInsuranceService
from src.services.patient_med_service import PatientMedServiceService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _alembic_config(db_url: str) -> Config:
    config = Config(str(PROJECT_ROOT / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", db_url)
    return config


def reset_database(db_url: str) -> None:
    config = _alembic_config(db_url)
    try:
        command.downgrade(config, "base")
    except Exception:
        pass
    command.upgrade(config, "head")


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:14") as container:
        yield container


@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7-alpine") as container:
        yield container


@pytest.fixture(scope="session")
def postgres_url(postgres_container: PostgresContainer) -> str:
    url = postgres_container.get_connection_url()
    return url.replace("psycopg2", "asyncpg")


@pytest.fixture(scope="session")
def redis_url(redis_container: RedisContainer) -> str:
    host = redis_container.get_container_host_ip()
    port = redis_container.get_exposed_port(6379)
    return f"redis://{host}:{port}/0"


@pytest.fixture
async def engine(postgres_url: str) -> AsyncGenerator[AsyncEngine, None]:
    await asyncio.to_thread(reset_database, postgres_url)
    engine = create_async_engine(postgres_url, pool_pre_ping=True)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def redis(redis_url: str) -> AsyncGenerator[Redis, None]:
    client = Redis.from_url(redis_url, decode_responses=True)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()


@pytest.fixture
def cache(redis: Redis) -> RedisCache:
    return RedisCache(redis, 3600)


@pytest.fixture
def doctor_service(session: AsyncSession, cache: RedisCache) -> DoctorAppointmentService:
    return DoctorAppointmentService(session, cache)


@pytest.fixture
def patient_service(session: AsyncSession, cache: RedisCache) -> PatientMedServiceService:
    return PatientMedServiceService(session, cache)


@pytest.fixture
def med_card_service(session: AsyncSession, cache: RedisCache) -> MedCardInsuranceService:
    return MedCardInsuranceService(session, cache)


@pytest.fixture
async def client(
    engine: AsyncEngine,
    cache: RedisCache,
) -> AsyncGenerator[AsyncClient, None]:
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
            yield session

        async def override_get_cache() -> RedisCache:
            return cache

        app = get_app()
        app.dependency_overrides[get_session] = override_get_session
        app.dependency_overrides[get_cache] = override_get_cache

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as http_client:
            yield http_client

        app.dependency_overrides.clear()
        await session.rollback()
