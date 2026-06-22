from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.common import NameStr


class PatientBase(BaseModel):
    name: NameStr


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
