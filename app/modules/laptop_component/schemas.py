from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class ComponentOrder(BaseModel):
    order_id: UUID
    component_id: UUID
    quantity: int

    class Config:
        orm_mode = True


class ComponentOrderData(ComponentOrder):
    component_order_id: UUID


class ComponentOrderResponse(BaseModel):
    status: int
    message: Optional[str]
    data: List[ComponentOrderData]
