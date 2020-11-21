import datetime
from uuid import UUID

from django.test import TestCase

from api import api
from api.models import Customer, Product, ProductionCapability, Batch, Policy


class TestPydantic(TestCase):

    def setUp(self) -> None:
        self.customer = Customer.objects.create(name="Julian", image="", address="", lat=0, lon=0)
        self.product = Product.objects.create(name="Kartoffel", description="", image="", unit="kg", handling="none")
        self.capability = ProductionCapability.objects.create(farm=self.customer, product=self.product,
                                                              monthly_quantity=15)
        self.batch = Batch.objects.create(capability=self.capability, details="", comment="", expected_amount=15.0,
                                          production_price=100.0, expected_price=150.0,
                                          expected_ready_date=datetime.datetime.today())
        self.policy = Policy.objects.create(batch=self.batch, hedged_price=100.0, due_date=datetime.datetime.today())

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

    def test_create_damage_report(self):
        damage_report_in = api.DamageReportIn(policy=self.policy.id)
        response = api.create_damage_report(damage_report_in)

        self.assertIsNotNone(response.id)

