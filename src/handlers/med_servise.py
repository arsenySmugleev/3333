from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from src.db import get_session
from src.models.med_service import MedService as MedServiceModel
from src.schemas.med_service import MedServiceCreate, MedServiceUpdate, MedService


router = APIRouter(tags=["med_service"], prefix="/med_service")


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session


@router.get("/{id}", response_model=MedService)
async def get_med_service(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(MedServiceModel).where(MedServiceModel.id == id))
    med_service = result.scalar_one_or_none()
    if not med_service:
        raise HTTPException(status_code=404, detail="MedService not found")
    return med_service


@router.post("/", response_model=MedService)
async def create_med_service(
        med_service_data: MedServiceCreate,
        session: AsyncSession = Depends(get_db_session)
):
    med_service_db = MedServiceModel(**med_service_data.model_dump())
    session.add(med_service_db)
    await session.commit()
    await session.refresh(med_service_db)
    return med_service_db


@router.patch("/{id}", response_model=MedService)
async def update_med_service(
        id: int,
        med_service_data: MedServiceUpdate,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(MedServiceModel).where(MedServiceModel.id == id))
    med_service_db = result.scalar_one_or_none()
    if not med_service_db:
        raise HTTPException(status_code=404, detail="MedService not found")
    update_med_service_data = med_service_data.model_dump(exclude_unset=True)
    for key, value in update_med_service_data.items():
        setattr(med_service_db, key, value)
    await session.commit()
    await session.refresh(med_service_db)
    return med_service_db


@router.delete("/{id}", status_code=204)
async def delete_med_service(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(MedServiceModel).where(MedServiceModel.id == id))
    med_service_db = result.scalar_one_or_none()
    if not med_service_db:
        raise HTTPException(status_code=404, detail="MedService not found")
    session.add(med_service_db)
    await session.delete(med_service_db)
    await session.commit()
    return None
