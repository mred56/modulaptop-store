from __future__ import annotations
from datetime import datetime
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory

from app.db.models.shipments import ShipmentsTable


class ShipmentsFactory(Factory):
    class Meta:
        model = ShipmentsTable

    shipment_id = factory.Faker("uuid4", cast_to=None)

    shipment_date = factory.Sequence(lambda n: datetime.strptime(
        f"2023-11-{(n % 30) + 1:02d}",
        "%Y-%m-%d"
    ))
    shipment_status = factory.Iterator(["pending", "shipped", "delivered"])
    shipment_address = factory.Sequence(lambda n: f"shipment_address_{n}")
