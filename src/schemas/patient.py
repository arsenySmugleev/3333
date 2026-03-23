from typing import Optional
from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    name: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None


class Patient(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
