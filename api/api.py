from typing import List
from uuid import UUID

from fastapi import APIRouter
from pydantic_django import PydanticDjangoModel

from api.models import Customer, Product, ProductionCapability, Batch, Policy

router = APIRouter()


class Customer_Pydantic(PydanticDjangoModel):
    class Config:
        model = Customer


class CustomerIn_Pydantic(PydanticDjangoModel):
    class Config:
        model = Customer
        exclude = ["id"]


class Product_Pydantic(PydanticDjangoModel):
    class Config:
        model = Product


class ProductIn_Pydantic(PydanticDjangoModel):
    class Config:
        model = Product
        exclude = ["id"]


class Capability_Pydantic(PydanticDjangoModel):
    class Config:
        model = ProductionCapability


class CapabilityIn_Pydantic(PydanticDjangoModel):
    class Config:
        model = ProductionCapability
        exclude = ["id", "batches"]


class Batch_Pydantic(PydanticDjangoModel):
    class Config:
        model = Batch


class BatchIn_Pydantic(PydanticDjangoModel):
    class Config:
        model = Batch
        exclude = ["id"]


class Policy_Pydantic(PydanticDjangoModel):
    class Config:
        model = Policy


class PolicyIn_Pydantic(PydanticDjangoModel):
    class Config:
        model = Policy
        exclude = ["id"]


@router.get("/customers", response_model=List[Customer_Pydantic], tags=["customer"])
def get_customers():
    """
    List all Customers
    """
    return list(map(lambda user: Customer_Pydantic.from_django(user), Customer.objects.all()))


@router.post("/customer", response_model=Customer_Pydantic, tags=["customer"], operation_id="create_customer")
def create_customer(customer: CustomerIn_Pydantic):
    created_customer = Customer.objects.create(**customer.dict(exclude_unset=True))
    return Customer_Pydantic.from_django(created_customer)


@router.get(
    "/customer/{customer_id}", response_model=Customer_Pydantic, tags=["customer"])
def get_customer(customer_id: UUID):
    return Customer_Pydantic.from_django(Customer.objects.get(id=customer_id))


@router.get(
    "/customer/{customer_id}/batches", response_model=List[Batch_Pydantic]
    , tags=["customer"])
def get_customer_batches(customer_id: UUID):
    queryset = Batch.objects.filter(batch__capability__farm__id=customer_id)
    return list(map(lambda batch: Batch_Pydantic.from_django(batch), queryset))


@router.post("/capability", response_model=Capability_Pydantic, tags=["customer"])
def create_capability(capability: CapabilityIn_Pydantic):
    farm = Customer.objects.get(id=capability.farm)
    product = Product.objects.get(id=capability.product)
    created_capability = ProductionCapability.objects.create(
        **capability.dict(exclude_unset=True, exclude={"farm", "product"}), farm=farm, product=product)
    return Capability_Pydantic.from_django(created_capability)


@router.post("/batches", response_model=List[Batch_Pydantic], tags=["policy"])
def get_batches():
    return list(map(lambda batch: Batch_Pydantic.from_django(batch), Batch.objects.all()))


@router.post("/batch", response_model=Batch_Pydantic, tags=["policy"])
def create_batch(batch: BatchIn_Pydantic):
    created_batch = Batch.objects.create(**batch.dict(exclude_unset=True))
    return Batch_Pydantic.from_django(created_batch)


@router.get("/policies", response_model=List[Policy_Pydantic], tags=["policy"])
def get_policies():
    return list(map(lambda policy: Policy_Pydantic.from_django(policy), Policy.objects.all()))


@router.post("/policy", response_model=Policy_Pydantic, tags=["policy"])
def create_policy(policy: PolicyIn_Pydantic):
    created_policy = Policy.objects.create(**policy.dict(exclude_unset=True))
    return Policy_Pydantic.from_django(created_policy)


@router.get(
    "/policy/{policy_id}", response_model=Policy_Pydantic, tags=["policy"])
def get_policy(policy_id: UUID):
    return Policy_Pydantic.from_django(Policy.get(id=policy_id))


@router.get("/products", response_model=List[Product_Pydantic], tags=["product"])
def get_products():
    return list(map(lambda p: Product_Pydantic.from_django(p), Product.objects.all()))


@router.post("/product", response_model=Product_Pydantic, tags=["product"])
def create_customer(product: ProductIn_Pydantic):
    created_product = Product.objects.create(**product.dict(exclude_unset=True))
    return Product_Pydantic.from_django(created_product)
