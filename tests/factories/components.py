from __future__ import annotations
import random
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory
from app.db.models.components import ComponentsTable


class ComponentsFactory(Factory):
    class Meta:
        model = ComponentsTable

    component_id = factory.Faker("uuid4", cast_to=None)

    type = factory.Sequence(lambda n: f"type_{n}")
    description = factory.Sequence(lambda n: f"description_{n}")
    make_year = factory.LazyFunction(lambda: random.randint(2019, 2023))
