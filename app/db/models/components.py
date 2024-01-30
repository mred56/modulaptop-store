from uuid import uuid4
from sqlalchemy import UUID, Integer, String
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.component_order import ComponentOrderTable
from app.db.models.laptops_components import LaptopsComponentsTable


class ComponentsTable(Base):
    __tablename__ = "components"

    component_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False
    )

    type: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    make_year: Mapped[int] = mapped_column(Integer, nullable=False)

    laptops = relationship(
        "LaptopsTable",
        secondary=LaptopsComponentsTable.__table__,
        back_populates="components"
    )  # type: ignore
    orders = relationship(
        "OrdersTable",
        secondary=ComponentOrderTable.__table__,
        back_populates="components"
    )
