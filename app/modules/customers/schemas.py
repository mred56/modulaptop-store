from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, constr, validator


# Data validation for sending to DB
class Customer(BaseModel):
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    email: Optional[EmailStr]

    @validator('email')
    def check_email_length(cls, value):
        if value and len(value) > 50:
            raise ValueError('Email must be at most 50 characters long')
        return value

    class Config:
        orm_mode = True


class PatchCustomer(Customer):
    first_name: Optional[constr(max_length=50)]
    last_name: Optional[constr(max_length=50)]


class CustomerData(Customer):
    customer_id: UUID


# Data validation for response
class StandardCustomersResponse(BaseModel):
    status: int
    message: Optional[str]
    data: List[CustomerData]


class StandardCustomerResponse(BaseModel):
    status: int
    message: Optional[str]
    data: CustomerData


class DeleteCustomerResponse(BaseModel):
    status: int
    message: Optional[str]
