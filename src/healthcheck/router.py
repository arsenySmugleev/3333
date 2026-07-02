from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
