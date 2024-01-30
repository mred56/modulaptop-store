from typing import List
from app.modules.components.schemas import (
    ComponentData,
    StandardComponentResponse
)
from app.modules.laptops.schemas import LaptopData, StandardLaptopResponse


class ComponentLaptopsData(ComponentData):
    laptops: List[LaptopData]


class ComponentLaptopsResponse(StandardComponentResponse):
    data: ComponentLaptopsData


class LaptopComponentsData(LaptopData):
    components: List[ComponentData]


class LaptopComponentsResponse(StandardLaptopResponse):
    data: LaptopComponentsData
