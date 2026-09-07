import pytest
from pydantic import ValidationError

from src.schemas.insurance import InsuranceCreate
from src.schemas.med_card import MedCardCreate


def test_snils_rejects_invalid_length():
    with pytest.raises(ValidationError):
        MedCardCreate(patient_name="Ivan", snils="123")


def test_snils_accepts_eleven_digits():
    med_card = MedCardCreate(patient_name="Ivan", snils="10940730177")
    assert med_card.snils == "10940730177"


def test_policy_number_must_be_positive():
    with pytest.raises(ValidationError):
        InsuranceCreate(policy_number=0)
