from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.common import OptionalNameStr
from src.schemas.patient import Patient, PatientBase
from src.schemas.med_service import MedService, MedServiceCreate
from src.models.patient import Patient as PatientModel


class PatientWithMedServiceCreate(PatientBase):
    med_service: List[MedServiceCreate]
    model_config = ConfigDict(from_attributes=True)

    def map_data(self) -> PatientModel:
        orm_med_service = MedServiceCreate.map_list(self.med_service)
        patient_dict = self.model_dump(exclude={"med_service"})
        patient = PatientModel(**patient_dict)
        patient.med_service = orm_med_service
        return patient


class PatientWithMedServiceUpdate(BaseModel):
    name: OptionalNameStr = None
    med_service_ids: Optional[List[UUID]] = None
    model_config = ConfigDict(from_attributes=True)

    def map_patient_dict(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude={"med_service_ids"})


class PatientWithMedServiceResponse(Patient):
    med_service: List[MedService]
