from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    name: str


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None


class Doctor(DoctorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PatientBase(BaseModel):
    name: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None


class Patient(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MedServiceBase(BaseModel):
    service_name: str


class MedServiceCreate(MedServiceBase):
    pass


class MedServiceUpdate(BaseModel):
    service_name: Optional[str] = None


class MedService(MedServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AppointmentBase(BaseModel):
    doc_id: int
    time_start: datetime
    patient_id: int
    med_service_id: int


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    doc_id: Optional[int] = None
    time_start: Optional[datetime] = None
    patient_id: Optional[int] = None
    med_service_id: Optional[int] = None


class Appointment(AppointmentBase):
    doctor: Optional[Doctor] = None
    patient: Optional[Patient] = None
    med_service: Optional[MedService] = None
    model_config = ConfigDict(from_attributes=True)


class MedCardBase(BaseModel):
    insurance_id: int


class MedCardCreate(MedCardBase):
    pass


class MedCardUpdate(BaseModel):
    insurance_id: Optional[int] = None


class MedCard(MedCardBase):
    id: int
    insurance: Optional["Insurance"] = None
    model_config = ConfigDict(from_attributes=True)


class InsuranceBase(BaseModel):
    med_card_id: int


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceUpdate(BaseModel):
    med_card_id: Optional[int] = None


class Insurance(InsuranceBase):
    id: int
    med_card: Optional[MedCard] = None
    model_config = ConfigDict(from_attributes=True)
