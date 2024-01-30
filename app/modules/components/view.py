from uuid import UUID
from fastapi import APIRouter, Depends
from app.base.dependencies.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.components import ComponentsTable

from app.modules.components.schemas import (
    ComponentData,
    Component,
    CreateComponentResponse,
    PatchComponent,
    StandardComponentResponse,
    DeleteComponentResponse,
)
from app.modules.laptops_components.schemas import (
    ComponentLaptopsData,
    ComponentLaptopsResponse
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
@router.post("/api/components", tags=["components"], response_model=CreateComponentResponse)
async def create_component(
    insert_data: Component,
    session: AsyncSession = Depends(get_session)
):
    component: ComponentsTable = await insert_into(
        session=session, table_schema=ComponentsTable, insert_data=insert_data
    )

    return CreateComponentResponse(
        status=201,
        message="Component created successfully",
        data=ComponentData.from_orm(component),
    )


# READ - all
@router.get("/api/components", tags=["components"], response_model=StandardComponentResponse)
async def get_components(session: AsyncSession = Depends(get_session)):
    components: list[ComponentsTable] = await select_all(
        session=session,
        table_schema=ComponentsTable
    )

    return StandardComponentResponse(
        status=200,
        message="Components retrieved successfully",
        data=[ComponentData.from_orm(component) for component in components],
    )


# READ - specific
@router.get("/api/components/{component_id}", tags=["components"], response_model=CreateComponentResponse)
async def get_component(
    component_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    component: ComponentsTable = await select_specific(
        session=session, table_schema=ComponentsTable, id=component_id
    )

    return CreateComponentResponse(
        status=200,
        message="Component retrieved successfully",
        data=ComponentData.from_orm(component),
    )


# UPDATE
@router.patch("/api/components/{component_id}", tags=["components"], response_model=CreateComponentResponse)
async def update_component(
    component_id: UUID,
    update_data: PatchComponent,
    session: AsyncSession = Depends(get_session)
):
    update_data_dict = update_data.dict(exclude_none=True, exclude_unset=True)

    component: ComponentsTable = await update_record(
        session=session, table_schema=ComponentsTable,
        id=component_id,
        update_data=update_data
    )

    if len(update_data_dict) == 0:
        return CreateComponentResponse(
            status=400,
            message="No data to update, please check your data.",
            data=ComponentData.from_orm(component)
        )

    return CreateComponentResponse(
        status=200,
        message="Component updated successfully",
        data=ComponentData.from_orm(component),
    )


# DELETE
@router.delete("/api/components/{component_id}", tags=["components"], response_model=DeleteComponentResponse)
async def delete_laptop(
    component_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    await delete_record(
        session=session,
        table_schema=ComponentsTable,
        id=component_id
    )

    return DeleteComponentResponse(
        status=200,
        message="Component deleted successfully"
    )


# READ - Component compatible laptops
@router.get("/api/components/{component_id}/laptops", tags=["laptops"], response_model=ComponentLaptopsResponse,)
async def get_laptop_components(
    component_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    component: ComponentsTable = await select_specific_extended(
        session=session,
        table_schema=ComponentsTable,
        id=component_id,
        attribute_name="laptops"
    )

    return ComponentLaptopsResponse(
        status=200,
        message="Component compatible laptops retrieved successfully",
        data=ComponentLaptopsData.from_orm(component),
    )
