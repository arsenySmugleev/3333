from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.schemas.common import NameStr


class DoctorBase(BaseModel):
    name: NameStr
    specialty: NameStr


class Doctor(DoctorBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
