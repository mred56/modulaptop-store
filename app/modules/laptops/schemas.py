from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, constr


# Data validation for sending to DB
class Laptop(BaseModel):
    manufacturer: constr(max_length=20)
    model: constr(max_length=20)
    make_year: int

    class Config:
        orm_mode = True


class PatchLaptop(Laptop):
    manufacturer: Optional[constr(max_length=20)]
    model: Optional[constr(max_length=20)]
    make_year: Optional[int]


class LaptopData(Laptop):
    laptop_id: UUID


# Data validation for response
class StandardLaptopResponse(BaseModel):
    status: int
    message: Optional[str]
    data: List[LaptopData]


class CreateLaptopResponse(StandardLaptopResponse):
    data: LaptopData


class DeleteLaptopResponse(BaseModel):
    status: int
    message: Optional[str]
