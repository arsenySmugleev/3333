from fastapi import APIRouter, status

from src.healthcheck.schemas import HealthcheckResponse

router = APIRouter(tags=["health"])


@router.get(
    "/healthcheck",
    response_model=HealthcheckResponse
)
async def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse()
