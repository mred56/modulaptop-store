from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.dependencies.db import get_session
from app.db.models.components import ComponentsTable
from app.db.models.laptops import LaptopsTable
from app.db.models.laptops_components import LaptopsComponentsTable
from app.modules.laptops_components.schemas import (
    LaptopComponentsData,
    LaptopComponentsResponse
)
from app.modules.laptops.schemas import (
    CreateLaptopResponse,
    Laptop,
    PatchLaptop,
    LaptopData,
    StandardLaptopResponse,
    DeleteLaptopResponse,
)
from app.modules.servicer import (
    delete_record,
    insert_into,
    select_all,
    select_specific,
    select_specific_extended,
    update_record,
)


router = APIRouter()


# CREATE
@router.post("/api/laptops", tags=["laptops"], response_model=CreateLaptopResponse)
async def create_laptop(
    insert_data: Laptop,
    session: AsyncSession = Depends(get_session)
):
    laptop: LaptopsTable = await insert_into(
        session=session,
        table_schema=LaptopsTable,
        insert_data=insert_data
    )

    return CreateLaptopResponse(
        status=201,
        message="Laptop created successfully",
        data=LaptopData.from_orm(laptop)
    )


# READ - all orders
@router.get("/api/laptops", tags=["laptops"], response_model=StandardLaptopResponse)
async def get_laptops(session: AsyncSession = Depends(get_session)):
    laptops = await select_all(session=session, table_schema=LaptopsTable)

    return StandardLaptopResponse(
        status=200,
        message="Laptops retrieved successfully",
        data=[LaptopData.from_orm(laptop) for laptop in laptops],
    )


# READ - specific order
@router.get("/api/laptops/{laptop_id}", tags=["laptops"], response_model=StandardLaptopResponse)
async def get_laptop(
    laptop_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    laptop: LaptopsTable = await select_specific(
        session=session,
        table_schema=LaptopsTable,
        id=laptop_id
    )

    return StandardLaptopResponse(
        status=200,
        message="Laptop retrieved successfully",
        data=[LaptopData.from_orm(laptop)]
    )


# UPDATE
@router.patch("/api/laptops/{laptop_id}", tags=["laptops"], response_model=CreateLaptopResponse)
async def update_laptop(
    laptop_id: UUID,
    update_data: PatchLaptop,
    session: AsyncSession = Depends(get_session)
):
    update_data_dict = update_data.dict(exclude_none=True, exclude_unset=True)

    laptop: LaptopsTable = await update_record(
        session=session,
        table_schema=LaptopsTable,
        id=laptop_id,
        update_data=update_data
    )

    if len(update_data_dict) == 0:
        return CreateLaptopResponse(
            status=400,
            message="No data to update, please check your data.",
            data=LaptopData.from_orm(laptop)
        )

    return CreateLaptopResponse(
        status=200,
        message="Laptop updated successfully",
        data=LaptopData.from_orm(laptop)
    )


# DELETE
@router.delete("/api/laptops/{laptop_id}", tags=["laptops"], response_model=DeleteLaptopResponse)
async def delete_laptop(
    laptop_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    await delete_record(
        session=session,
        table_schema=LaptopsTable,
        id=laptop_id
    )

    return DeleteLaptopResponse(
        status=200,
        message="Laptop deleted successfully"
    )


# CREATE - Add component to laptop
@router.post("/api/laptops/{laptop_id}/components/{component_id}", tags=["laptops"], response_model=LaptopComponentsResponse)
async def add_component(
    laptop_id: UUID,
    component_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    laptop: LaptopsTable = await select_specific_extended(
        session=session,
        table_schema=LaptopsTable,
        id=laptop_id,
        attribute_name="components"
    )
    component: ComponentsTable = await select_specific(
        session=session,
        table_schema=ComponentsTable,
        id=component_id
    )

    association = LaptopsComponentsTable(
        laptop_id=laptop.laptop_id,
        component_id=component.component_id
    )
    session.add(association)

    await session.commit()
    await session.refresh(laptop)

    return LaptopComponentsResponse(
        status=200,
        message="Laptop's component created successfully",
        data=LaptopComponentsData.from_orm(laptop),
    )


# READ - Laptop's components
@router.get("/api/laptops/{laptop_id}/components", tags=["laptops"], response_model=LaptopComponentsResponse)
async def get_laptop_components(
    laptop_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    laptop: LaptopsTable = await select_specific_extended(
        session=session,
        table_schema=LaptopsTable,
        id=laptop_id,
        attribute_name="components"
    )

    return LaptopComponentsResponse(
        status=200,
        message="Laptop's components retrieved successfully",
        data=LaptopComponentsData.from_orm(laptop),
    )
