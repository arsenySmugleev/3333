from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.models.association import patient_med_service_association
import sqlalchemy as sa
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from src.models.patient import Patient


class MedService(Base):
    __tablename__ = "med_services"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_name: Mapped[str] = mapped_column(sa.String())

    patient: Mapped[List["Patient"]] = relationship("Patient",
                                                     secondary=patient_med_service_association,
                                                     back_populates="med_service")
