from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from src.db import get_session
from src.models.insurance import Insurance as InsuranceModel
from src.schemas.insurance import Insurance, InsuranceCreate, InsuranceUpdate


router = APIRouter(prefix="/insurance", tags=["insurance"])


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session


@router.get("/{id}", response_model=Insurance)
async def get_insurance(
        id: int,
        session: AsyncSession = Depends(get_db_session)
) -> Insurance:
    stmt = select(InsuranceModel).where(InsuranceModel.id == id)
    result = await session.execute(stmt)
    insurance = result.scalar_one_or_none()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return insurance


@router.post("/", response_model=Insurance)
async def create_insurance(
        insurance_data: InsuranceCreate,
        session: AsyncSession = Depends(get_db_session)
):
    insurance_db = InsuranceModel(**insurance_data.model_dump())
    session.add(insurance_db)
    await session.commit()
    stmt = select(InsuranceModel).where(InsuranceModel.id == insurance_db.id)
    result = await session.execute(stmt)
    insurance_med_card = result.scalar_one_or_none()
    return insurance_med_card


@router.patch("/{id}", response_model=Insurance)
async def update_insurance(
        id: int,
        insurance_data: InsuranceUpdate,
        session: AsyncSession = Depends(get_db_session)
):
    stmt = select(InsuranceModel).where(InsuranceModel.id == id)
    result = await session.execute(stmt)
    insurance_db = result.scalar_one_or_none()
    if not insurance_db:
        raise HTTPException(status_code=404, detail="Insurance not found")
    updated_insurance_data = insurance_data.model_dump(exclude_unset=True)
    for key, value in updated_insurance_data.items():
        setattr(insurance_db, key, value)
    await session.commit()
    await session.refresh(insurance_db)
    return insurance_db


@router.delete("/{id}", status_code=204)
async def delete_insurance(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(InsuranceModel).where(InsuranceModel.id == id))
    insurance_db = result.scalar_one_or_none()
    if not insurance_db:
        raise HTTPException(status_code=404, detail="Insurance not found")
    await session.delete(insurance_db)
    await session.commit()
    return None
