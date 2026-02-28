from typing import List

import sqlalchemy as sa
from src.models.patient import Patient
from src.models.user import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MedService(Base):
    __tablename__ = "med_services"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(sa.String())

    patient: Mapped[List["Patient"]] = relationship(backpopulates="med_service",
                                                               ondelete="CASCADE")
