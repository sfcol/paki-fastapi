import uuid
from enum import Enum

from django.db import models


class Customer(models.Model):
    """
    Customer of the App / the SFC
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lat = models.DecimalField(decimal_places=6, max_digits=9, null=True)
    lon = models.DecimalField(decimal_places=6, max_digits=9, null=True)


class ProductUnits(str, Enum):
    """
    Unit in which the product is measured
    """
    WEIGHT_KG = 'KG'
    VOLUME_LITER = 'L'
    PIECE = 'PCS'


class Handling(str, Enum):
    """
    Does the Product need special handling?
    """
    REFRIGERATION = 'refrigeration'
    NONE = 'none'


class Product(models.Model):
    """
    One product which is supported for a policy like e.g. wheat, meat, ...
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    handling = models.CharField(max_length=255)


class ProductionCapability(models.Model):
    """
    A capability means that a farm (a Customer) produces one kind of Product.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey(Customer, related_name="capabilities", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="products", on_delete=models.CASCADE)
    monthly_quantity = models.DecimalField(decimal_places=6, max_digits=9, null=False, blank=False)


class Batch(models.Model):
    """
    A Batch of production
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    capability = models.ForeignKey(ProductionCapability, related_name="batches", on_delete=models.CASCADE)
    details = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    expected_amount = models.DecimalField(decimal_places=6, max_digits=9, null=False)
    production_price = models.DecimalField(decimal_places=6, max_digits=9, null=False)
    expected_price = models.DecimalField(decimal_places=6, max_digits=9, null=False)
    expected_ready_date = models.DateField()


class Policy(models.Model):
    """
    A policy is a PUT Option on a (defined) production amount that should be ready for delivery at a specific due date
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.OneToOneField(Batch, related_name="policy", on_delete=models.CASCADE)
    hedged_price = models.DecimalField(decimal_places=6, max_digits=9, null=False)
    due_date = models.DateField()

