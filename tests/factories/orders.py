from __future__ import annotations
from datetime import datetime
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory

from app.db.models.orders import OrdersTable
from app.db.models.shipments import ShipmentsTable
from tests.factories.customers import CustomersFactory
from tests.factories.shipments import ShipmentsFactory


class OrdersFactory(Factory):
    class Meta:
        model = OrdersTable

    order_id = factory.Faker("uuid4", cast_to=None)
    order_date = factory.Sequence(lambda n: datetime.strptime(
        f"2023-11-{(n % 30) + 1:02d}",
        "%Y-%m-%d"
    ))
    order_status = factory.Iterator(["pending", "in progress", "finished"])

    customer = factory.SubFactory(CustomersFactory)
    customer_id = factory.SelfAttribute("customer.customer_id")

    @factory.post_generation
    def set_shipment(self, create, extracted, **kwargs):
        if isinstance(extracted, ShipmentsTable):
            self.shipment = extracted
            self.shipment_id = self.shipment.shipment_id
        elif extracted is None or extracted is True:
            self.shipment = ShipmentsFactory()
            self.shipment_id = self.shipment.shipment_id
        else:
            self.shipment = None
            self.shipment_id = None
