from sqlalchemy import UUID, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class LaptopsComponentsTable(Base):
    __tablename__ = "laptops_components"

    laptop_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("laptops.laptop_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )

    component_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("components.component_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
