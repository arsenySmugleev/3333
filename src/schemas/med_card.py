from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MedCardBase(BaseModel):
    patient_name: str


class MedCardCreate(MedCardBase):
    pass


class MedCardUpdate(BaseModel):
    patient_name: Optional[str] = None


class MedCard(MedCardBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
