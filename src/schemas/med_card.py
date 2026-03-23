from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


if TYPE_CHECKING:
    from src.schemas.insurance import Insurance


class MedCardBase(BaseModel):
    insurance_id: int


class MedCardCreate(MedCardBase):
    pass


class MedCardUpdate(BaseModel):
    insurance_id: Optional[int] = None


class MedCard(MedCardBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
