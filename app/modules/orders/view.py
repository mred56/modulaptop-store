from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.dependencies.db import get_session
from app.db.models.component_order import ComponentOrderTable
from app.db.models.laptop_order import LaptopOrderTable
from app.db.models.orders import OrdersTable
from app.modules.laptop_component.schemas import (
    ComponentOrder,
    ComponentOrderData,

    ComponentOrderResponse
)
from app.modules.laptop_order.schemas import (
    LaptopOrder,
    LaptopOrderData,
    LaptopOrderResponse
)
from app.modules.orders.schemas import (
    DeleteOrderResponse,
    InsertOrder,
    OrderComponentsData,
    OrderComponentsResponse,
    OrderCustomerData,
    OrderCustomerResponse,
    OrdersComponentsResponse,
    OrdersCustomerResponse,
    OrderData,
    OrderLaptopsData,
    OrderLaptopsResponse,
    OrderShipmentData,
    OrderShipmentResponse,
    OrdersLaptopsResponse,
    OrdersShipmentResponse,
    PatchOrder,
    StandardOrdersResponse,
    StandardOrderResponse
)
from app.modules.servicer import (
    delete_record,
    insert_into,
    select_all,
    select_all_extended,
    select_specific,
    select_specific_extended,
    update_record
)


router = APIRouter()


# CREATE
@router.post("/api/orders", tags=["orders"], response_model=StandardOrderResponse)
async def create_order(
    order_data: InsertOrder,
    session: AsyncSession = Depends(get_session)
):
    order: OrdersTable = await insert_into(
        session=session,
        table_schema=OrdersTable,
        insert_data=order_data
    )

    return StandardOrderResponse(
        status=201,
        message="Order created successfully",
        data=OrderData.from_orm(order)
    )


# CREATE - add laptop to order
@router.post("/api/orders/laptop", tags=["orders"], response_model=LaptopOrderResponse)
async def add_laptop_to_order(
    laptop_order_data: LaptopOrder,
    session: AsyncSession = Depends(get_session)
):
    laptop_order: LaptopOrderTable = await insert_into(
        session=session,
        table_schema=LaptopOrderTable,
        insert_data=laptop_order_data
    )

    return LaptopOrderResponse(
        status=201,
        message="Laptop order created successfully",
        data=LaptopOrderData.from_orm(laptop_order)
    )


# CREATE - add component to order
@router.post("/api/orders/component", tags=["orders"], response_model=ComponentOrderResponse)
async def add_component_to_order(
    component_order_data: ComponentOrder,
    session: AsyncSession = Depends(get_session)
):
    laptop_order: ComponentOrderTable = await insert_into(
        session=session,
        table_schema=ComponentOrderTable,
        insert_data=component_order_data
    )

    return ComponentOrderResponse(
        status=201,
        message="Component order created successfully",
        data=[ComponentOrderData.from_orm(laptop_order)]
    )


# READ - all orders
@router.get("/api/orders", tags=["orders"], response_model=StandardOrdersResponse)
async def get_orders(
    session: AsyncSession = Depends(get_session)
):
    orders: list[OrdersTable] = await select_all(
        session=session,
        table_schema=OrdersTable
    )

    return StandardOrdersResponse(
        status=200,
        message="Orders sucessfully retrieved",
        data=[OrderData.from_orm(order) for order in orders]
    )


# READ - orders' customers
@router.get("/api/orders/customer", tags=['orders'], response_model=OrdersCustomerResponse)
async def get_orders_customer(
    session: AsyncSession = Depends(get_session)
):
    orders: list[OrdersTable] = await select_all_extended(
        session=session,
        table_schema=OrdersTable,
        attribute_name="customer"
    )

    return OrdersCustomerResponse(
        status=200,
        message="Orders sucessfully retrieved",
        data=[OrderCustomerData.from_orm(order) for order in orders]
    )


# READ - orders' shipments
@router.get("/api/orders/shipment", tags=['orders'], response_model=OrdersShipmentResponse)
async def get_orders_shipment(
    session: AsyncSession = Depends(get_session)
):
    orders: list[OrdersTable] = await select_all_extended(
        session=session,
        table_schema=OrdersTable,
        attribute_name="shipment"
    )

    return OrdersShipmentResponse(
        status=200,
        message="Orders sucessfully retrieved",
        data=[OrderShipmentData.from_orm(order) for order in orders]
    )


# READ - orders' laptops
@router.get("/api/orders/laptops", tags=['orders'], response_model=OrdersLaptopsResponse)
async def get_orders_laptops(
    session: AsyncSession = Depends(get_session)
):
    orders: list[OrdersTable] = await select_all_extended(
        session=session,
        table_schema=OrdersTable,
        attribute_name="laptops"
    )

    return OrdersLaptopsResponse(
        status=200,
        message="Orders sucessfully retrieved",
        data=[OrderLaptopsData.from_orm(order) for order in orders]
    )


# READ - orders' components
@router.get("/api/orders/components", tags=['orders'], response_model=OrdersComponentsResponse)
async def get_orders_components(
    session: AsyncSession = Depends(get_session)
):
    orders: list[OrdersTable] = await select_all_extended(
        session=session,
        table_schema=OrdersTable,
        attribute_name="components"
    )

    return OrdersComponentsResponse(
        status=200,
        message="Orders sucessfully retrieved",
        data=[OrderComponentsData.from_orm(order) for order in orders]
    )


# READ - specific order
@router.get("/api/orders/{order_id}", tags=["orders"], response_model=StandardOrderResponse)
async def get_order(
    order_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    order: OrdersTable = await select_specific(
        session=session,
        table_schema=OrdersTable,
        id=order_id
    )

    return StandardOrderResponse(
        status=200,
        message="Order sucessfully retrieved",
        data=OrderData.from_orm(order)
    )


# READ - specific order's customer
@router.get("/api/orders/{order_id}/customer", tags=['orders'], response_model=OrderCustomerResponse)
async def get_order_customer(
    order_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    order: OrdersTable = await select_specific_extended(
        session=session,
        table_schema=OrdersTable,
        id=order_id,
        attribute_name="customer"
    )

    return OrderCustomerResponse(
        status=200,
        message="Order sucessfully retrieved",
        data=OrderCustomerData.from_orm(order)
    )


# READ - specific order's shipment
@router.get("/api/orders/{order_id}/shipment", tags=['orders'], response_model=OrderShipmentResponse)
async def get_order_shipment(
    order_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    order: OrdersTable = await select_specific_extended(
        session=session,
        table_schema=OrdersTable,
        id=order_id,
        attribute_name="shipment"
    )

    return OrderShipmentResponse(
        status=200,
        message="Order sucessfully retrieved",
        data=OrderShipmentData.from_orm(order)
    )


# READ - specific order's laptops
@router.get("/api/orders/{order_id}/laptops", tags=['orders'], response_model=OrderLaptopsResponse)
async def get_order_laptops(
    order_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    order: OrdersTable = await select_specific_extended(
        session=session,
        table_schema=OrdersTable,
        id=order_id,
        attribute_name="laptops"
    )

    return OrderLaptopsResponse(
        status=200,
        message="Order sucessfully retrieved",
        data=OrderLaptopsData.from_orm(order)
    )


# READ - specific order's components
@router.get("/api/orders/{order_id}/components", tags=['orders'], response_model=OrderComponentsResponse)
async def get_order_components(
    order_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    order: OrdersTable = await select_specific_extended(
        session=session,
        table_schema=OrdersTable,
        id=order_id,
        attribute_name="components"
    )

    return OrderComponentsResponse(
        status=200,
        message="Order sucessfully retrieved",
        data=OrderComponentsData.from_orm(order)
    )


# UPDATE
@router.patch("/api/orders/{order_id}", tags=['orders'], response_model=StandardOrderResponse)
async def update_order(
    order_id: UUID,
    update_data: PatchOrder,
    session: AsyncSession = Depends(get_session)
):
    update_data_dict = update_data.dict(exclude_none=True, exclude_unset=True)

    order: OrdersTable = await update_record(
        session=session,
        table_schema=OrdersTable,
        id=order_id,
        update_data=update_data
    )

    if len(update_data_dict) == 0:
        return StandardOrderResponse(
            status=400,
            message="No data to update, please check your data.",
            data=OrderData.from_orm(order)
        )

    return StandardOrderResponse(
        status=200,
        message="Order updated successfully",
        data=OrderData.from_orm(order)
    )


# DELETE
@router.delete("/api/orders/{order_id}", tags=['orders'], response_model=DeleteOrderResponse)
async def delete_order(
    order_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    await delete_record(
        session=session,
        table_schema=OrdersTable,
        id=order_id
    )

    return DeleteOrderResponse(
        status=200,
        message="Order deleted successfully"
    )
