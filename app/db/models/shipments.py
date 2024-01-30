from datetime import date
from uuid import uuid4
from sqlalchemy import UUID, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ShipmentsTable(Base):
    __tablename__ = "shipments"

    shipment_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False
    )
    shipment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    shipment_status: Mapped[str] = mapped_column(String(20), nullable=False)
    shipment_address: Mapped[str] = mapped_column(String(100), nullable=False)

    orders = relationship('OrdersTable', back_populates="shipment")
