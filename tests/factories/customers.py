from __future__ import annotations
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory

from app.db.models.customers import CustomersTable


class CustomersFactory(Factory):
    class Meta:
        model = CustomersTable

    customer_id = factory.Faker("uuid4", cast_to=None)

    first_name = factory.Sequence(lambda n: f"user_{n}")
    last_name = factory.Sequence(lambda n: f"user_last_name_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
