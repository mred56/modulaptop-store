from __future__ import annotations
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory
from app.db.models.laptop_order import LaptopOrderTable


class LaptopOrderFactory(Factory):
    class Meta:
        model = LaptopOrderTable

    laptop_order_id = factory.Faker("uuid4", cast_to=None)

    laptop_id = factory.Faker('uuid4')
    order_id = factory.Faker('uuid4')

    quantity = factory.Faker("pyint")
