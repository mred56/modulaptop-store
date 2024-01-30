from __future__ import annotations
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory
from app.db.models.laptops_components import LaptopsComponentsTable


class LaptopsComponentsFactory(Factory):
    class Meta:
        model = LaptopsComponentsTable

    laptop_id = factory.Faker('uuid4')
    component_id = factory.Faker('uuid4')
