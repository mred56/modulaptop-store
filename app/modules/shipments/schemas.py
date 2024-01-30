import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, constr
from enum import Enum


class Status(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"


class Shipment(BaseModel):
    shipment_date: datetime.date
    shipment_status: Status
    shipment_address: constr(max_length=100)

    class Config:
        orm_mode = True


class PatchShipment(Shipment):
    shipment_date: Optional[datetime.date]
    shipment_status: Optional[Status]
    shipment_address: Optional[constr(max_length=100)]


class ShipmentData(Shipment):
    shipment_id: UUID


# Data validation for response
class StandardShipmentsResponse(BaseModel):
    status: int
    message: Optional[str]
    data: List[ShipmentData]


class StandardShipmentResponse(BaseModel):
    status: int
    message: Optional[str]
    data: ShipmentData


class DeleteShipmentResponse(BaseModel):
    status: int
    message: Optional[str]
