import datetime
from uuid import UUID

from django.test import TestCase

from api import api
from api.models import Customer, Product, ProductionCapability


class TestPydantic(TestCase):

    def setUp(self) -> None:
        self.customer = Customer.objects.create(name="Julian", image="", address="", lat=0, lon=0)
        self.product = Product.objects.create(name="Kartoffel", description="", image="", unit="kg", handling="none")
        self.capability = ProductionCapability.objects.create(farm=self.customer, product=self.product,
                                                              monthly_quantity=15)

    def test_create_capability(self):
        cap_in = api.CapabilityIn_Pydantic(farm=self.customer.id, product=self.product.id, monthly_quantity=5)
        response = api.create_capability(cap_in)

        self.assertIsNotNone(response.id)

    def test_create_batch(self):
        batch_in = api.BatchIn_Pydantic(capability=self.capability.id, details="", comment="", expected_amount=15.0,
                                        production_price=100, expected_price=150,
                                        expected_ready_date=datetime.datetime.today())
        response = api.create_batch(batch_in)

        self.assertIsNotNone(response.id)
        self.assertIsInstance(response.capability, UUID)
