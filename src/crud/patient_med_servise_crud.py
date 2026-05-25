from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from src.models.patient import Patient as PatientModel
from src.models.med_service import MedService as MedServiceModel
from src.schemas.med_service import MedServiceCreate
from src.schemas.patient import PatientCreate


class PatientMedServiceCrud:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_patient_with_med_service(self, patient_id: int) -> PatientModel:
        result = await self.session.execute(
            select(PatientModel).where(PatientModel.id == patient_id).
            options(selectinload(PatientModel.med_service))
        )
        patient = result.scalar_one_or_none()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    async def create_patient_with_med_service(self,
                                              patient_data: PatientCreate,
                                              med_service_data: MedServiceCreate):
        patient = PatientModel(**patient_data.model_dump())
        med_service = MedServiceModel(**med_service_data.model_dump())
        patient.med_service.append(med_service)
        self.session.add(patient)
        await self.session.flush()
        return patient

    async def update_patient_with_med_service(self, patient_id: int, med_service_ids: list[int]):
        patient = await self.get_patient_with_med_service(patient_id)
        stmt_services = select(MedServiceModel).where(MedServiceModel.id.in_(med_service_ids))
        result_services = await self.session.execute(stmt_services)
        new_services = result_services.scalars().all()
        patient.med_service = new_services
        await self.session.flush()
        return patient

    async def delete_patient_or_med_service(self,
                                            patient_id: int = None,
                                            med_service_id: int = None,
                                            delete_type: str = "patient"  # "patient", "med_service"
                                            ) -> None:
        """
        delete_type:
            "patient" - удалить пациента
            "med_service" - удалить услугу
        """

        if delete_type.lower() == "patient" and patient_id:
            patient = await self.get_patient_with_med_service(patient_id)
            await self.session.delete(patient)
            await self.session.flush()

        elif delete_type.lower() == "med_service" and med_service_id:
            result = await self.session.execute(
                select(MedServiceModel).where(MedServiceModel.id == med_service_id)
            )
            med_service = result.scalar_one_or_none()
            await self.session.delete(med_service)
            await self.session.flush()

        return None
