import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions.exceptions import NotFoundException
from src.models.patient import Patient as PatientModel
from src.models.med_service import MedService as MedServiceModel
from src.schemas.patient import (
    PatientWithMedServiceCreate,
    PatientWithMedServiceResponse,
    PatientWithMedServiceUpdate,
)

logger = logging.getLogger(__name__)


class PatientMedServiceService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_patient_model(self, patient_id: UUID) -> PatientModel:
        result = await self.session.execute(
            select(PatientModel)
            .where(
                PatientModel.id == patient_id,
                PatientModel.is_deleted.is_(False),
            )
            .options(selectinload(PatientModel.med_service))
        )
        patient = result.scalar_one_or_none()
        if not patient:
            message = f"Patient {patient_id} not found"
            logger.warning(message)
            raise NotFoundException(message)
        return patient

    async def get_patient_with_med_service(self, patient_id: UUID) -> PatientWithMedServiceResponse:
        patient = await self._get_patient_model(patient_id)
        return PatientWithMedServiceResponse.from_model(patient)

    async def create_patient_with_med_service(
        self,
        patient_data: PatientWithMedServiceCreate,
    ) -> PatientWithMedServiceResponse:
        patient = patient_data.map_data()
        self.session.add(patient)
        await self.session.flush()
        await self.session.refresh(patient, attribute_names=["med_service"])
        return PatientWithMedServiceResponse.from_model(patient)

    async def update_patient_with_med_service(
        self,
        patient_id: UUID,
        update_data: PatientWithMedServiceUpdate,
    ) -> PatientWithMedServiceResponse:
        patient = await self._get_patient_model(patient_id)
        patient_dict = update_data.map_patient_dict()
        if patient_dict:
            for key, value in patient_dict.items():
                setattr(patient, key, value)

        if update_data.med_service_ids is not None:
            stmt_services = select(MedServiceModel).where(
                MedServiceModel.id.in_(update_data.med_service_ids),
                MedServiceModel.is_deleted.is_(False),
            )
            result_services = await self.session.execute(stmt_services)
            new_services = result_services.scalars().all()
            if len(new_services) != len(update_data.med_service_ids):
                message = (
                    f"One or more med services not found for ids: {update_data.med_service_ids}"
                )
                logger.warning(message)
                raise NotFoundException(message)
            patient.med_service = new_services

        await self.session.flush()
        await self.session.refresh(patient, attribute_names=["med_service"])
        return PatientWithMedServiceResponse.from_model(patient)

    async def delete_patient_or_med_service(
        self,
        patient_id: UUID = None,
        med_service_id: UUID = None,
        delete_type: str = "patient",
    ) -> None:
        if delete_type.lower() == "patient" and patient_id:
            patient = await self._get_patient_model(patient_id)
            patient.is_deleted = True
            await self.session.flush()

        elif delete_type.lower() == "med_service" and med_service_id:
            result = await self.session.execute(
                select(MedServiceModel).where(
                    MedServiceModel.id == med_service_id,
                    MedServiceModel.is_deleted.is_(False),
                )
            )
            med_service = result.scalar_one_or_none()
            if not med_service:
                message = f"MedService {med_service_id} not found"
                logger.warning(message)
                raise NotFoundException(message)
            med_service.is_deleted = True
            await self.session.flush()
