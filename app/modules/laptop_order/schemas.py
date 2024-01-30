from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class LaptopOrder(BaseModel):
    order_id: UUID
    laptop_id: UUID
    quantity: int

    class Config:
        orm_mode = True


class LaptopOrderData(LaptopOrder):
    laptop_order_id: UUID


class LaptopOrderResponse(BaseModel):
    status: int
    message: Optional[str]
    data: LaptopOrderData
