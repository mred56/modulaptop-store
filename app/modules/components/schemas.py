from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, constr


# Data validation for sending to DB
class Component(BaseModel):
    type: constr(max_length=20)
    description: Optional[constr(max_length=150)]
    make_year: int

    class Config:
        orm_mode = True


class PatchComponent(Component):
    type: Optional[constr(max_length=20)]
    make_year: Optional[int]


class ComponentData(Component):
    component_id: UUID


# Data validation for response
class StandardComponentResponse(BaseModel):
    status: int
    message: Optional[str]
    data: List[ComponentData]


class CreateComponentResponse(StandardComponentResponse):
    data: ComponentData


class DeleteComponentResponse(BaseModel):
    status: int
    message: Optional[str]
