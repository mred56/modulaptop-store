import datetime
from uuid import uuid4
from sqlalchemy import UUID, Date, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.component_order import ComponentOrderTable
from app.db.models.laptop_order import LaptopOrderTable


class OrdersTable(Base):
    __tablename__ = "orders"

    order_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False
    )
    order_date: Mapped[datetime.date] = mapped_column(Date(), nullable=False)
    order_status: Mapped[str] = mapped_column(String(20), nullable=False)

    customer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False
    )

    shipment_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shipments.shipment_id", ondelete="CASCADE"),
        nullable=True
    )

    customer = relationship("CustomersTable", back_populates="orders")
    shipment = relationship("ShipmentsTable", back_populates="orders")
    laptops = relationship(
        "LaptopsTable",
        secondary=LaptopOrderTable.__table__,
        back_populates="orders"
    )
    components = relationship(
        "ComponentsTable",
        secondary=ComponentOrderTable.__table__,
        back_populates="orders"
    )
