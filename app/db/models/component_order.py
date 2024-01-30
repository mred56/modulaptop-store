from uuid import uuid4
from sqlalchemy import UUID, ForeignKey, Integer
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class ComponentOrderTable(Base):
    __tablename__ = "component_order"

    component_order_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4, nullable=False
    )

    order_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False
    )

    component_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("components.component_id", ondelete="CASCADE"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
