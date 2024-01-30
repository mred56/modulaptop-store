import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.modules.components.schemas import ComponentData
from app.modules.customers.schemas import (
    CustomerData,
    StandardCustomerResponse
)
from app.modules.laptops.schemas import LaptopData

from app.modules.shipments.schemas import (
    ShipmentData,
    StandardShipmentResponse
)


class Status(str, Enum):
    pending = "pending"
    shipped = "in progress"
    delivered = "finished"


class Order(BaseModel):
    order_date: datetime.date
    order_status: Status
    shipment_id: Optional[UUID]

    class Config:
        orm_mode = True


class PatchOrder(Order):
    order_date: Optional[datetime.date]
    order_status: Optional[Status]


class InsertOrder(Order):
    customer_id: UUID


class OrderData(Order):
    order_id: UUID
    customer_id: UUID


class ShipmentOrdersData(ShipmentData):
    orders: List[OrderData]


class OrderShipmentData(OrderData):
    # shipment_id can be omitted at order creation time
    shipment: Optional[ShipmentData] = None


class CustomerOrdersData(CustomerData):
    orders: List[OrderData]


class OrderCustomerData(OrderData):
    customer: CustomerData


class OrderLaptopsData(OrderData):
    laptops: List[LaptopData]


class OrderComponentsData(OrderData):
    components: List[ComponentData]


# Data validation for response
class StandardOrdersResponse(BaseModel):
    status: int
    message: Optional[str]
    data: List[OrderData]


class StandardOrderResponse(BaseModel):
    status: int
    message: Optional[str]
    data: OrderData


class ShipmentsOrdersResponse(StandardShipmentResponse):
    data: List[ShipmentOrdersData]


class ShipmentOrdersResponse(StandardShipmentResponse):
    data: ShipmentOrdersData


class OrdersShipmentResponse(StandardOrderResponse):
    data: List[OrderShipmentData]


class OrderShipmentResponse(StandardOrderResponse):
    data: OrderShipmentData


class OrdersCustomerResponse(StandardOrderResponse):
    data: List[OrderCustomerData]


class OrderCustomerResponse(StandardOrderResponse):
    data: OrderCustomerData


class OrdersLaptopsResponse(StandardOrderResponse):
    data: List[OrderLaptopsData]


class OrderLaptopsResponse(StandardOrderResponse):
    data: OrderLaptopsData


class OrdersComponentsResponse(StandardOrderResponse):
    data: List[OrderComponentsData]


class OrderComponentsResponse(StandardOrderResponse):
    data: OrderComponentsData


class CustomersOrdersResponse(StandardCustomerResponse):
    data: List[CustomerOrdersData]


class CustomerOrdersResponse(StandardCustomerResponse):
    data: CustomerOrdersData


class DeleteOrderResponse(BaseModel):
    status: int
    message: Optional[str]
