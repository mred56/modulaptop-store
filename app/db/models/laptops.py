from uuid import uuid4
from sqlalchemy import UUID, Integer, String
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.laptop_order import LaptopOrderTable
from app.db.models.laptops_components import LaptopsComponentsTable


class LaptopsTable(Base):
    __tablename__ = "laptops"

    laptop_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4, nullable=False
    )
    manufacturer: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(20), nullable=False)
    make_year: Mapped[int] = mapped_column(Integer, nullable=False)

    components = relationship(
        "ComponentsTable",
        secondary=LaptopsComponentsTable.__table__,
        back_populates="laptops"
    )  # type: ignore
    orders = relationship(
        "OrdersTable",
        secondary=LaptopOrderTable.__table__,
        back_populates="laptops"
    )
