from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.models.insurance import Insurance


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