from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.models.patient import Patient as PatientModel
from src.schemas.patient import Patient, PatientCreate, PatientUpdate
from src.db import get_session


router = APIRouter(prefix="/patient", tags=["patient"])


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session


@router.get("/{id}", response_model=Patient)
async def get_patient(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(PatientModel).where(PatientModel.id == id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", response_model=Patient)
async def create_patient(
        patient_data: PatientCreate,
        session: AsyncSession = Depends(get_db_session)
):
    patient_db = PatientModel(**patient_data.model_dump())
    session.add(patient_db)
    await session.commit()
    stmt = select(PatientModel).where(PatientModel.id == patient_db.id).options(selectinload(PatientModel.med_service))
    result = await session.execute(stmt)
    patient_db = result.scalar_one_or_none()
    return patient_db


@router.patch("/{id}", response_model=Patient)
async def update_patient(
        id: int,
        patient_data: PatientUpdate,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(PatientModel).where(PatientModel.id == id))
    patient_db = result.scalar_one_or_none()
    if not patient_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    updated_patient_data = patient_data.model_dump(exclude_unset=True)
    for key, value in updated_patient_data.items():
        setattr(patient_db, key, value)
    await session.commit()
    await session.refresh(patient_db)
    return patient_db


@router.delete("/{id}", status_code=204)
async def delete_patient(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(PatientModel).where(PatientModel.id == id))
    patient_db = result.scalar_one_or_none()
    if not patient_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    await session.delete(patient_db)
    await session.commit()
    return None
