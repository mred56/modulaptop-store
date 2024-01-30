from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.dependencies.db import get_session
from app.db.models.customers import CustomersTable
from app.modules.customers.schemas import (
    CustomerData,
    Customer,
    PatchCustomer,
    StandardCustomersResponse,
    StandardCustomerResponse,
    DeleteCustomerResponse,
)
from app.modules.orders.schemas import (
    CustomerOrdersData,
    CustomerOrdersResponse,
    CustomersOrdersResponse
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
@router.post("/api/customers", tags=["customers"], response_model=StandardCustomerResponse)
async def create_customer(
    customer_data: Customer,
    session: AsyncSession = Depends(get_session)
):
    customer: CustomersTable = await insert_into(
        session=session,
        table_schema=CustomersTable,
        insert_data=customer_data
    )

    return StandardCustomerResponse(
        status=201,
        message="Customer created successfully",
        data=CustomerData.from_orm(customer)
    )


# READ
@router.get("/api/customers", tags=["customers"], response_model=StandardCustomersResponse)
async def get_customers(session: AsyncSession = Depends(get_session)):
    customers: list[CustomersTable] = await select_all(
        session=session,
        table_schema=CustomersTable
    )

    return StandardCustomersResponse(
        status=200,
        message="Customers sucessfully retrieved",
        data=[CustomerData.from_orm(customer) for customer in customers],
    )


# READ - customers' orders
@router.get("/api/customers/orders", tags=["customers"], response_model=CustomersOrdersResponse)
async def get_customers_orders(session: AsyncSession = Depends(get_session)):
    customers: list[CustomersTable] = await select_all_extended(
        session=session,
        table_schema=CustomersTable,
        attribute_name="orders"
    )

    return CustomersOrdersResponse(
        status=200,
        message="Customers sucessfully retrieved",
        data=[CustomerOrdersData.from_orm(customer) for customer in customers],
    )


# READ - specific customer
@router.get("/api/customers/{customer_id}", tags=["customers"], response_model=StandardCustomerResponse)
async def get_customer(
    customer_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    customer: CustomersTable = await select_specific(
        session=session,
        table_schema=CustomersTable,
        id=customer_id
    )

    return StandardCustomerResponse(
        status=200,
        message="Customer sucessfully retrieved",
        data=CustomerData.from_orm(customer)
    )


# READ - specific customer's orders
@router.get(
    "/api/customers/{customer_id}/orders", tags=["customers"], response_model=CustomerOrdersResponse
)
async def get_customer_orders(
    customer_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    customer: CustomersTable = await select_specific_extended(
        session=session,
        table_schema=CustomersTable,
        id=customer_id,
        attribute_name="orders"
    )

    return CustomerOrdersResponse(
        status=200,
        message="Customer and orders sucessfully retrieved",
        data=CustomerOrdersData.from_orm(customer),
    )


# UPDATE
@router.patch("/api/customers/{customer_id}", tags=["customers"], response_model=StandardCustomerResponse)
async def update_customer(
    customer_id: UUID,
    update_data: PatchCustomer,
    session: AsyncSession = Depends(get_session)
):
    update_data_dict = update_data.dict(exclude_none=True, exclude_unset=True)

    customer = await update_record(
        session=session,
        table_schema=CustomersTable,
        id=customer_id,
        update_data=update_data
    )

    if len(update_data_dict) == 0:
        return StandardCustomerResponse(
            status=400,
            message="No data to update, please check your data.",
            data=CustomerData.from_orm(customer)
        )

    return StandardCustomerResponse(
        status=200,
        message="Customer updated successfully",
        data=CustomerData.from_orm(customer)
    )


# DELETE
@router.delete("/api/customers/{customer_id}", tags=["customers"], response_model=DeleteCustomerResponse)
async def delete_customer(
    customer_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    await delete_record(
        session=session,
        table_schema=CustomersTable,
        id=customer_id
    )

    return DeleteCustomerResponse(
        status=200,
        message="Customer deleted successfully"
    )
