from uuid import uuid4

import pytest

from src.exceptions.exceptions import NotFoundException
from src.schemas.insurance import InsuranceCreate, InsuranceUpdate
from src.schemas.med_card import (
    MedCardCreate,
    MedCardInsuranceCreate,
    MedCardInsuranceUpdate,
    MedCardUpdate,
)
from src.services.med_card_insurance import MedCardInsuranceService


def _create_payload(
    patient_name: str = "Ivan",
    snils: str = "10940730177",
    policy_number: int = 1315,
) -> MedCardInsuranceCreate:
    return MedCardInsuranceCreate(
        med_card=MedCardCreate(patient_name=patient_name, snils=snils),
        insurance=InsuranceCreate(policy_number=policy_number),
    )


@pytest.mark.asyncio
async def test_create_and_get_med_card(med_card_service: MedCardInsuranceService):
    created = await med_card_service.create_med_card_with_insurance(_create_payload())

    assert created.patient_name == "Ivan"
    assert created.snils == "10940730177"
    assert created.insurance.policy_number == 1315

    fetched = await med_card_service.get_med_card_with_insurance(created.id)
    assert fetched.id == created.id
    assert fetched.insurance.policy_number == created.insurance.policy_number


@pytest.mark.asyncio
async def test_get_med_card_not_found(med_card_service: MedCardInsuranceService):
    with pytest.raises(NotFoundException):
        await med_card_service.get_med_card_with_insurance(uuid4())


@pytest.mark.asyncio
async def test_get_med_card_uses_cache(med_card_service: MedCardInsuranceService, redis):
    created = await med_card_service.create_med_card_with_insurance(_create_payload())
    cache_key = med_card_service._cache_key(created.id)

    assert await redis.get(cache_key) is None

    await med_card_service.get_med_card_with_insurance(created.id)
    cached = await redis.get(cache_key)
    assert cached is not None
    assert "Ivan" in cached

    await redis.set(cache_key, cached.replace("Ivan", "CachedName"))
    fetched = await med_card_service.get_med_card_with_insurance(created.id)
    assert fetched.patient_name == "CachedName"


@pytest.mark.asyncio
async def test_update_invalidates_cache(med_card_service: MedCardInsuranceService, redis):
    created = await med_card_service.create_med_card_with_insurance(_create_payload())
    await med_card_service.get_med_card_with_insurance(created.id)
    cache_key = med_card_service._cache_key(created.id)
    assert await redis.get(cache_key) is not None

    updated = await med_card_service.update_med_card_with_insurance(
        created.id,
        MedCardInsuranceUpdate(
            med_card=MedCardUpdate(patient_name="Petr"),
            insurance=InsuranceUpdate(policy_number=9999),
        ),
    )
    assert updated.patient_name == "Petr"
    assert updated.insurance.policy_number == 9999
    assert await redis.get(cache_key) is None


@pytest.mark.asyncio
async def test_delete_soft_deletes_and_invalidates_cache(
    med_card_service: MedCardInsuranceService,
    redis,
):
    created = await med_card_service.create_med_card_with_insurance(_create_payload())
    await med_card_service.get_med_card_with_insurance(created.id)
    cache_key = med_card_service._cache_key(created.id)

    await med_card_service.delete_med_card_with_insurance(created.id)

    assert await redis.get(cache_key) is None
    with pytest.raises(NotFoundException):
        await med_card_service.get_med_card_with_insurance(created.id)
