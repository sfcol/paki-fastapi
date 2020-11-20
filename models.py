from enum import Enum
from uuid import UUID

import tortoise
from pydantic import BaseModel
from tortoise import Model, fields, Tortoise, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import CASCADE


class Customer(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    address = fields.CharField(max_length=255)
    lat = fields.DecimalField(decimal_places=6, max_digits=9, null=True)
    lon = fields.DecimalField(decimal_places=6, max_digits=9, null=True)


Customer_Pydantic = pydantic_model_creator(Customer, name="Customer")
CustomerIn_Pydantic = pydantic_model_creator(Customer, name="CustomerIn", exclude_readonly=True)


class ProductUnits(str, Enum):
    WEIGHT_KG = 'KG'
    VOLUME_LITER = 'L'
    PIECE = 'PCS'


class Handling(str, Enum):
    REFRIGERATION = 'refrigeration'
    NONE = 'none'


class Product(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)
    image = fields.CharField(max_length=255)
    unit = ProductUnits
    handling = Handling


Product_Pydantic = pydantic_model_creator(Product, name="Product")
ProductIn_Pydantic = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)


class ProductionCapability(Model):
    id = fields.UUIDField(pk=True)
    farm = fields.ForeignKeyField("models.Customer", related_name="capabilities", on_delete=fields.CASCADE)
    product = fields.ForeignKeyField("models.Product", related_name="capabilities", on_delete=fields.CASCADE)
    monthly_quantity = fields.DecimalField(decimal_places=6, max_digits=9, null=False)


tortoise.Tortoise.init_models(["models"], "models")

Capability_Pydantic = pydantic_model_creator(ProductionCapability, name="Capability")
CapabilityIn_Pydantic = pydantic_model_creator(ProductionCapability, name="CapabilityIn", exclude_readonly=True)


class Policy(Model):
    id = fields.UUIDField(pk=True)
    capability = fields.ForeignKeyField("models.ProductionCapability", related_name="policies", on_delete=CASCADE)
    price = fields.DecimalField(decimal_places=6, max_digits=9, null=False)
    due_date = fields.DateField()


Policy_Pydantic = pydantic_model_creator(Policy, name="Policy")
PolicyIn_Pydantic = pydantic_model_creator(Policy, name="PolicyIn", exclude_readonly=True)
