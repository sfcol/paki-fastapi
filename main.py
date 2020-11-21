from typing import List
from uuid import UUID

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

from models import Customer_Pydantic, CustomerIn_Pydantic, Customer, Capability_Pydantic, CapabilityIn_Pydantic, \
    ProductionCapability, Product_Pydantic, Product, ProductIn_Pydantic, Policy_Pydantic, Policy, PolicyIn_Pydantic, \
    Batch_Pydantic, Batch, BatchIn_Pydantic

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/customers", response_model=List[Customer_Pydantic], tags=["customer"])
async def get_customers():
    """
    List all Customers
    """
    return await Customer_Pydantic.from_queryset(Customer.all())


@app.post("/customer", response_model=Customer_Pydantic, tags=["customer"], operation_id="create_customer")
async def create_customer(customer: CustomerIn_Pydantic):
    created_customer = await Customer.create(**customer.dict(exclude_unset=True))
    return await Customer_Pydantic.from_tortoise_orm(created_customer)


@app.get(
    "/customer/{customer_id}", response_model=Customer_Pydantic, responses={404: {"model": HTTPNotFoundError}}
    , tags=["customer"])
async def get_customer(customer_id: UUID):
    return await Customer_Pydantic.from_queryset_single(Customer.get(id=customer_id))


@app.put(
    "/customer/{customer_id}", response_model=Customer_Pydantic, responses={404: {"model": HTTPNotFoundError}}
    , tags=["customer"])
async def update_customer(customer_id: UUID, customer: CustomerIn_Pydantic):
    await Customer.filter(id=customer_id).update(**customer.dict(exclude_unset=True))
    return await Customer_Pydantic.from_queryset_single(Customer.get(id=customer_id))


@app.get(
    "/customer/{customer_id}/batches", response_model=List[Batch_Pydantic],
    responses={404: {"model": HTTPNotFoundError}}
    , tags=["customer"])
async def get_customer_batches(customer_id: UUID):
    return await Batch_Pydantic.from_queryset(Batch.filter(batch__capability__farm__id=customer_id))


@app.post("/capability", response_model=Capability_Pydantic, tags=["customer"])
async def create_capability(capability: CapabilityIn_Pydantic):
    created_capability = await ProductionCapability.create(**capability.dict(exclude_unset=True))
    return await Capability_Pydantic.from_tortoise_orm(created_capability)


@app.post("/batches", response_model=List[Batch_Pydantic], tags=["policy"])
async def get_batches():
    return await Batch_Pydantic.from_queryset(Batch.all())


@app.post("/batch", response_model=Batch_Pydantic, tags=["policy"])
async def create_batch(batch: BatchIn_Pydantic):
    created_batch = await Batch.create(**batch.dict(exclude_unset=True))
    return await Capability_Pydantic.from_tortoise_orm(created_batch)


@app.get("/policies", response_model=List[Policy_Pydantic], tags=["policy"])
async def get_policy():
    return await Policy_Pydantic.from_queryset(Policy.all())


@app.post("/policy", response_model=Policy_Pydantic, tags=["policy"])
async def create_policy(policy: PolicyIn_Pydantic):
    created_policy = await Policy.create(**policy.dict(exclude_unset=True))
    return await Policy_Pydantic.from_tortoise_orm(created_policy)


@app.get(
    "/policy/{policy_id}", response_model=Policy_Pydantic, responses={404: {"model": HTTPNotFoundError}}
    , tags=["policy"])
async def get_policy(policy_id: UUID):
    return await Policy_Pydantic.from_queryset_single(Policy.get(id=policy_id))


@app.get("/products", response_model=List[Product_Pydantic], tags=["product"])
async def get_products():
    return await Product_Pydantic.from_queryset(Product.all())


@app.post("/product", response_model=Product_Pydantic, tags=["product"])
async def create_customer(product: ProductIn_Pydantic):
    created_product = await Product.create(**product.dict(exclude_unset=True))
    return await Product_Pydantic.from_tortoise_orm(created_product)


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
