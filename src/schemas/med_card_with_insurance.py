from pydantic import ConfigDict

from src.schemas.insurance import Insurance
from src.schemas.med_card import MedCard


class MedCardInsuranceResponse(MedCard):
    insurance: "Insurance"
    model_config = ConfigDict(from_attributes=True)
