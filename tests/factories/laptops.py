from __future__ import annotations
import random
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory
from app.db.models.laptops import LaptopsTable


class LaptopsFactory(Factory):
    class Meta:
        model = LaptopsTable

    laptop_id = factory.Faker("uuid4", cast_to=None)

    manufacturer = factory.Sequence(lambda n: f"manufacturer_{n}")
    model = factory.Sequence(lambda n: f"model_{n}")
    make_year = factory.LazyFunction(lambda: random.randint(2019, 2023))
