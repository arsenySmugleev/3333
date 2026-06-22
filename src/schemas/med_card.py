from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.schemas.common import NameStr, OptionalNameStr


class MedCardBase(BaseModel):
    patient_name: NameStr


class MedCardCreate(MedCardBase):
    pass


class MedCardUpdate(BaseModel):
    patient_name: OptionalNameStr = None


class MedCard(MedCardBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
