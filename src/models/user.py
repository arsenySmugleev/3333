import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeMeta, Mapped, declarative_base, mapped_column

from uuid import UUID, uuid4

metadata = sa.MetaData()


class BaseServiceModel:
    """Базовый класс для таблиц сервиса."""

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None


Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)


class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    username: Mapped[str] = mapped_column(sa.String())

class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String())

class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeingKey("doctors.id"), ondelete="CASCADE")
    time_start :Mapped[datetime.datetime]=mapped_column(sa.DateTime())
    patient_id: Mapped[int] = mapped_column(Foreingkey('patients.id'), ondelete="CASACADE")
    med_service_id: Mapped[int] mapped_column(Foreingkey('med_services.id'), ondelete="CASACADE")

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String())

class MedServices(Base):
    __tablename__ = "med_services"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(sa.String())

class MedCard(Base):
    __tablename__ = "med_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    insurance_id: Mapped[int] mapped_column(Foreingkey('insurances.id'), ondelete="CASACADE")

class Insurance(Base):
    __tablename__ = "insurances"
    id: Mapped[int] = mapped_column(primary_key=True)
    med_card_id: Mapped[int] mapped_column(Foreingkey('med_cards.id'), ondelete="CASACADE")