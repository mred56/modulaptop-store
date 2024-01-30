from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.dependencies.db import get_session
from app.db.models.shipments import ShipmentsTable
from app.modules.orders.schemas import (
    ShipmentOrdersData,
    ShipmentsOrdersResponse,
    ShipmentOrdersResponse
)
from app.modules.shipments.schemas import (
    DeleteShipmentResponse,
    ShipmentData,
    Shipment,
    PatchShipment,
    StandardShipmentResponse,
    StandardShipmentsResponse,
    Status,
)
from app.modules.servicer import (
    delete_record,
    insert_into,
    select_all,
    select_all_extended,
    select_specific,
    select_specific_extended,
    update_record,
)


router = APIRouter()


# CREATE
@router.post("/api/shipments", tags=["shipments"], response_model=StandardShipmentResponse)
async def insert_shipment(
    shipment_data: Shipment,
    session: AsyncSession = Depends(get_session)
):
    shipment: ShipmentsTable = await insert_into(
        session=session,
        table_schema=ShipmentsTable,
        insert_data=shipment_data
    )

    return StandardShipmentResponse(
        status=201,
        message="Shipment created successfully",
        data=ShipmentData.from_orm(shipment)
    )


# READ - all shipments
@router.get("/api/shipments", tags=["shipments"], response_model=StandardShipmentsResponse)
async def get_shipments(session: AsyncSession = Depends(get_session)):
    shipments: list[ShipmentsTable] = await select_all(
        session=session,
        table_schema=ShipmentsTable
    )

    return StandardShipmentsResponse(
        status=200,
        message="Shipments sucessfully retrieved",
        data=[ShipmentData.from_orm(shipment) for shipment in shipments],
    )


# READ - shipments' orders
@router.get("/api/shipments/orders", tags=["shipments"], response_model=ShipmentsOrdersResponse)
async def get_shipments_orders(session: AsyncSession = Depends(get_session)):
    shipments: list[ShipmentsTable] = await select_all_extended(
        session=session,
        table_schema=ShipmentsTable,
        attribute_name="orders"
    )

    return ShipmentsOrdersResponse(
        status=200,
        message="Shipments sucessfully retrieved",
        data=[ShipmentOrdersData.from_orm(shipment) for shipment in shipments],
    )


# READ - specific shipment
@router.get("/api/shipments/{shipment_id}", tags=["shipments"], response_model=StandardShipmentResponse)
async def get_shipment(
    shipment_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    shipment: ShipmentsTable = await select_specific(
        session=session,
        table_schema=ShipmentsTable,
        id=shipment_id
    )

    return StandardShipmentResponse(
        status=200,
        message="Shipment sucessfully retrieved",
        data=ShipmentData.from_orm(shipment)
    )


# READ - specific shipment's orders
@router.get("/api/shipments/{shipment_id}/orders", tags=["shipments"], response_model=ShipmentOrdersResponse)
async def get_shipment_orders(
    shipment_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    shipment: ShipmentsTable = await select_specific_extended(
        session=session,
        table_schema=ShipmentsTable,
        id=shipment_id,
        attribute_name="orders"
    )

    return ShipmentOrdersResponse(
        status=200,
        message="Shipment and orders sucessfully retrieved",
        data=ShipmentOrdersData.from_orm(shipment),
    )


# READ - filter by shipment status
@router.get("/api/shipments/status/{shipment_status}", tags=["shipments"], response_model=StandardShipmentsResponse)
async def filter_by_status(
    shipment_status: Status,
    session: AsyncSession = Depends(get_session)
):
    query = (
        select(ShipmentsTable).
        where(ShipmentsTable.shipment_status == shipment_status)
    )

    response = await session.execute(query)
    shipments = response.scalars().all()

    return StandardShipmentsResponse(
        status=200,
        message="Shipments filtered successfully",
        data=[ShipmentData.from_orm(shipment) for shipment in shipments]
    )


# UPDATE
@router.patch(
    "/api/shipments/{shipment_id}", tags=["shipments"], response_model=StandardShipmentResponse
)
async def patch_shipment(
    shipment_id: UUID,
    update_data: PatchShipment,
    session: AsyncSession = Depends(get_session)
):
    update_data_dict = update_data.dict(exclude_none=True, exclude_unset=True)

    shipment: ShipmentsTable = await update_record(
        session=session,
        table_schema=ShipmentsTable,
        id=shipment_id,
        update_data=update_data
    )

    if len(update_data_dict) == 0:
        return StandardShipmentResponse(
            status=400,
            message="No data to update, please check your data.",
            data=ShipmentData.from_orm(shipment)
        )

    return StandardShipmentResponse(
        status=200,
        message="Shipment updated successfully",
        data=ShipmentData.from_orm(shipment)
    )


# DELETE
@router.delete(
    "/api/shipments/{shipment_id}",
    tags=["shipments"],
    response_model=DeleteShipmentResponse
)
async def delete_shipment(
    shipment_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    await delete_record(
        session=session,
        table_schema=ShipmentsTable,
        id=shipment_id
    )

    return DeleteShipmentResponse(
        status=200,
        message="Shipment deleted successfully"
    )
