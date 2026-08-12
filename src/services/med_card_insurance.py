import logging
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config import Settings
from src.exceptions.exceptions import NotFoundException
from src.models.insurance import Insurance as InsuranceModel
from src.models.med_card import MedCard as MedCardModel
from src.schemas.med_card import (
    MedCardInsuranceCreate,
    MedCardInsuranceResponse,
    MedCardInsuranceUpdate,
)

logger = logging.getLogger(__name__)
settings = Settings()


class MedCardInsuranceService:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

    @staticmethod
    def _cache_key(med_card_id: UUID) -> str:
        return f"med_card:{med_card_id}"

    async def _invalidate_cache(self, med_card_id: UUID) -> None:
        await self.redis.delete(self._cache_key(med_card_id))

    async def _get_med_card_model(self, med_card_id: UUID) -> MedCardModel:
        result = await self.session.execute(
            select(MedCardModel)
            .where(
                MedCardModel.id == med_card_id,
                MedCardModel.is_deleted.is_(False),
            )
            .options(
                selectinload(
                    MedCardModel.insurance.and_(InsuranceModel.is_deleted.is_(False))
                )
            )
            .execution_options(populate_existing=True)
        )
        med_card = result.scalar_one_or_none()
        if not med_card:
            message = f"MedCard {med_card_id} not found"
            logger.warning(message)
            raise NotFoundException(message)
        return med_card

    async def get_med_card_with_insurance(self, med_card_id: UUID) -> MedCardInsuranceResponse:
        cache_key = self._cache_key(med_card_id)
        cached = await self.redis.get(cache_key)
        if cached is not None:
            return MedCardInsuranceResponse.model_validate_json(cached)

        med_card = await self._get_med_card_model(med_card_id)
        response = MedCardInsuranceResponse.from_model(med_card)
        await self.redis.set(
            cache_key,
            response.model_dump_json(),
            ex=settings.cache_ttl_seconds,
        )
        return response

    async def create_med_card_with_insurance(
        self,
        med_card_data: MedCardInsuranceCreate,
    ) -> MedCardInsuranceResponse:
        med_card = med_card_data.map_data()
        self.session.add(med_card)
        await self.session.flush()
        med_card = await self._get_med_card_model(med_card.id)
        return MedCardInsuranceResponse.from_model(med_card)

    async def update_med_card_with_insurance(
        self,
        med_card_id: UUID,
        update_data: MedCardInsuranceUpdate,
    ) -> MedCardInsuranceResponse:
        med_card = await self._get_med_card_model(med_card_id)
        update_data.apply_to(med_card)
        await self.session.flush()
        await self._invalidate_cache(med_card_id)
        med_card = await self._get_med_card_model(med_card_id)
        return MedCardInsuranceResponse.from_model(med_card)

    async def delete_med_card_with_insurance(self, med_card_id: UUID) -> None:
        med_card = await self._get_med_card_model(med_card_id)
        med_card.is_deleted = True
        if med_card.insurance is not None:
            med_card.insurance.is_deleted = True
        await self.session.flush()
        await self._invalidate_cache(med_card_id)
