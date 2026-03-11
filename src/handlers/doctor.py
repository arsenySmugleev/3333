from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db import get_session
from src.schemas.doctor import Doctor, DoctorCreate, DoctorUpdate
from src.models.doctor import Doctor as DoctorModel

router = APIRouter(prefix="/doctor", tags=["doctor"])


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session


@router.get("/{id}", response_model=Doctor)
async def get_doctor(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(DoctorModel).where(DoctorModel.id == id))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.post("/", response_model=Doctor)
async def create_doctor(
        doctor_data: DoctorCreate,
        session: AsyncSession = Depends(get_db_session)
):
    db_doctor = DoctorModel(**doctor_data.model_dump())
    session.add(db_doctor)
    await session.commit()
    await session.refresh(db_doctor)
    return db_doctor


@router.patch("/{id}", response_model=Doctor)
async def update_doctor(
        id: int,
        doctor_data: DoctorUpdate,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(DoctorModel).where(DoctorModel.id == id))
    db_doctor = result.scalar_one_or_none()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    updated_doctor_data = doctor_data.model_dump(exclude_unset=True)
    for key, value in updated_doctor_data.items():
        setattr(db_doctor, key, value)
    await session.commit()
    await session.refresh(db_doctor)
    return db_doctor


@router.delete("/{id}", status_code=204)
async def delete_doctor(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(DoctorModel).where(DoctorModel.id == id))
    db_doctor = result.scalar_one_or_none()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    await session.delete(db_doctor)
    await session.commit()
    return f"Doctor with id{DoctorModel.id} delete"
