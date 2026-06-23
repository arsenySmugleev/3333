from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions.exceptions import MedServiceNotFoundException, PatientNotFoundException
from src.models.patient import Patient as PatientModel
from src.models.med_service import MedService as MedServiceModel
from src.schemas.patient_with_med_service import PatientWithMedServiceCreate, PatientWithMedServiceUpdate


class PatientMedServiceCrud:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_patient_with_med_service(self, patient_id: UUID) -> PatientModel:
        result = await self.session.execute(
            select(PatientModel).where(PatientModel.id == patient_id).
            options(selectinload(PatientModel.med_service))
        )
        patient = result.scalar_one_or_none()
        if not patient:
            raise PatientNotFoundException(patient_id)
        return patient

    async def create_patient_with_med_service(self, patient_data: PatientWithMedServiceCreate):
        patient = patient_data.map_data()
        self.session.add(patient)
        await self.session.flush()
        return patient

    async def update_patient_with_med_service(
            self,
            patient_id: UUID,
            update_data: PatientWithMedServiceUpdate
    ):
        patient = await self.get_patient_with_med_service(patient_id)
        patient_dict = update_data.map_patient_dict()
        if patient_dict:
            for key, value in patient_dict.items():
                setattr(patient, key, value)

        if update_data.med_service_ids is not None:
            stmt_services = select(MedServiceModel).where(MedServiceModel.id.in_(update_data.med_service_ids))
            result_services = await self.session.execute(stmt_services)
            new_services = result_services.scalars().all()
            if len(new_services) != len(update_data.med_service_ids):
                raise MedServiceNotFoundException()
            patient.med_service = new_services

        await self.session.flush()
        return patient

    async def delete_patient_or_med_service(self,
                                            patient_id: UUID = None,
                                            med_service_id: UUID = None,
                                            delete_type: str = "patient"  # "patient", "med_service"
                                            ) -> None:

        if delete_type.lower() == "patient" and patient_id:
            patient = await self.get_patient_with_med_service(patient_id)
            await self.session.delete(patient)
            await self.session.flush()

        elif delete_type.lower() == "med_service" and med_service_id:
            result = await self.session.execute(
                select(MedServiceModel).where(MedServiceModel.id == med_service_id)
            )
            med_service = result.scalar_one_or_none()
            if not med_service:
                raise MedServiceNotFoundException(med_service_id)
            await self.session.delete(med_service)
            await self.session.flush()

        return None
