from typing import Optional
from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    name: str
    specialty: str


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None


class Doctor(DoctorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
