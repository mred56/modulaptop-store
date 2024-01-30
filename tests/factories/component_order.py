from __future__ import annotations
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory
from app.db.models.component_order import ComponentOrderTable


class ComponentOrderFactory(Factory):
    class Meta:
        model = ComponentOrderTable

    component_order_id = factory.Faker("uuid4", cast_to=None)

    component_id = factory.Faker('uuid4')
    order_id = factory.Faker('uuid4')

    quantity = factory.Faker("pyint")
