from enum import Enum
from typing import List

import tortoise
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise import Model, fields
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from tortoise.contrib.pydantic import pydantic_model_creator

from models import Customer_Pydantic, CustomerIn_Pydantic, Customer, Capability_Pydantic, CapabilityIn_Pydantic, \
    ProductionCapability, Product_Pydantic, Product, ProductIn_Pydantic, Policy_Pydantic, Policy, PolicyIn_Pydantic

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


#
# class Contact(BaseModel):
#     id: uuid.UUID
#     email: EmailStr
#     name: str
#     picture: str
#     favorite_boxes: List[uuid.UUID]
#
#
# class ShipmentSizes(str, Enum):
#     S = 'S'
#     M = 'M'
#     L = 'L'
#     XL = 'XL'
#
#
# class DropoffStatus(str, Enum):
#     ACCEPTED = 'accepted'
#     DENIED = 'denied'
#
#
# # Step 1
# class SendRequest(BaseModel):
#     """
#     I want to drop you something off
#     Sender -> Backend -> Receiver
#     """
#     id: uuid.UUID
#     sender: uuid.UUID
#     receiver: uuid.UUID
#     box: uuid.UUID
#     size: ShipmentSizes
#     dropoff_date: date
#
#
# # Step 2
# class SendResponse(BaseModel):
#     """
#     I accept and will pick it up
#     Receiver -> Backend
#     """
#     request: SendRequest
#     status: DropoffStatus
#     pickup_date: date
#
#
# # Step 3
# class ShipmentConfirmation(BaseModel):
#     """
#     You have a DEAL!
#     Backend -> Sender
#     Backend -> Receiver
#     """
#     sender: EmailStr
#     receiver: EmailStr
#     box: uuid.UUID
#     size: ShipmentSizes
#     dropoff_date: date
#     pickup_date: date
#
#
# requests = []

@app.get("/customers", response_model=List[Customer_Pydantic], tags=["customer"])
async def get_customers():
    return await Customer_Pydantic.from_queryset(Customer.all())


@app.post("/customer", response_model=Customer_Pydantic, tags=["customer"])
async def create_customer(customer: CustomerIn_Pydantic):
    created_customer = await Customer.create(**customer.dict(exclude_unset=True))
    return await Customer_Pydantic.from_tortoise_orm(created_customer)


@app.get(
    "/customer/{customer_id}", response_model=Customer_Pydantic, responses={404: {"model": HTTPNotFoundError}}
    , tags=["customer"])
async def get_customer(customer_id: int):
    return await Customer_Pydantic.from_queryset_single(Customer.get(id=customer_id))


@app.put(
    "/customer/{customer_id}", response_model=Customer_Pydantic, responses={404: {"model": HTTPNotFoundError}}
    , tags=["customer"])
async def update_customer(customer_id: int, customer: CustomerIn_Pydantic):
    await Customer.filter(id=customer_id).update(**customer.dict(exclude_unset=True))
    return await Customer_Pydantic.from_queryset_single(Customer.get(id=customer_id))


@app.post("/capability", response_model=Capability_Pydantic, tags=["customer"])
async def create_customer(capability: CapabilityIn_Pydantic):
    created_capability = await ProductionCapability.create(**capability.dict(exclude_unset=True))
    return await Capability_Pydantic.from_tortoise_orm(created_capability)


@app.get("/policies", response_model=List[Policy_Pydantic], tags=["customer"])
async def get_policy():
    return await Policy_Pydantic.from_queryset(Policy.all())


@app.post("/policy", response_model=Policy_Pydantic, tags=["customer"])
async def create_customer(policy: PolicyIn_Pydantic):
    created_policy = await Policy.create(**policy.dict(exclude_unset=True))
    return await Policy_Pydantic.from_tortoise_orm(created_policy)


@app.get(
    "/policy/{policy_id}", response_model=Policy_Pydantic, responses={404: {"model": HTTPNotFoundError}}
    , tags=["customer"])
async def get_policy(policy_id: int):
    return await Policy_Pydantic.from_queryset_single(Policy.get(id=policy_id))


@app.get("/products", response_model=List[Product_Pydantic], tags=["product"])
async def get_products():
    return await Product_Pydantic.from_queryset(Product.all())


@app.post("/product", response_model=Product_Pydantic, tags=["product"])
async def create_customer(product: ProductIn_Pydantic):
    created_product = await Product.create(**product.dict(exclude_unset=True))
    return await Product_Pydantic.from_tortoise_orm(created_product)


# #################################################################
# # User CRUD
# #################################################################
#
# @app.get("/users", response_model=List[User_Pydantic], tags=["user"])
# async def get_users():
#     return await User_Pydantic.from_queryset(User.all())
#
#
# @app.post("/user", response_model=User_Pydantic, tags=["user"])
# async def create_user(user: UserIn_Pydantic):
#     created_user = await User.create(**user.dict(exclude_unset=True))
#     return await User_Pydantic.from_tortoise_orm(created_user)
#
#
# @app.get(
#     "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
#     , tags=["user"])
# async def get_user(user_id: int):
#     return await User_Pydantic.from_queryset_single(User.get(id=user_id))
#
#
# @app.put(
#     "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
#     , tags=["user"])
# async def update_user(user_id: int, user: UserIn_Pydantic):
#     await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
#     return await User_Pydantic.from_queryset_single(User.get(id=user_id))
#
#
# class Status(BaseModel):
#     message: str
#
#
# @app.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}},
#             tags=["user"])
# async def delete_user(user_id: int):
#     deleted_count = await User.filter(id=user_id).delete()
#     if not deleted_count:
#         raise HTTPException(status_code=404, detail=f"User {user_id} not found")
#     return Status(message=f"Deleted user {user_id}")
#
#
# # End User CRUD
#
# #################################################################
# # Box CRUD
# #################################################################
#
# @app.get("/boxes", response_model=List[Box_Pydantic], tags=["box"])
# async def get_boxes():
#     return await Box_Pydantic.from_queryset(Box.all())
#
#
# @app.post("/box", response_model=Box_Pydantic, tags=["box"])
# async def create_user(box: BoxIn_Pydantic):
#     created_box = await Box.create(**box.dict(exclude_unset=True))
#     return await Box_Pydantic.from_tortoise_orm(created_box)
#
#
# # @app.get(
# #     "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
# # )
# # async def get_user(user_id: int):
# #     return await User_Pydantic.from_queryset_single(User.get(id=user_id))
# #
# #
# # @app.put(
# #     "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
# # )
# # async def update_user(user_id: int, user: UserIn_Pydantic):
# #     await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
# #     return await User_Pydantic.from_queryset_single(User.get(id=user_id))
# #
# #
# # class Status(BaseModel):
# #     message: str
# #
# #
# # @app.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
# # async def delete_user(user_id: int):
# #     deleted_count = await User.filter(id=user_id).delete()
# #     if not deleted_count:
# #         raise HTTPException(status_code=404, detail=f"User {user_id} not found")
# #     return Status(message=f"Deleted user {user_id}")
#
#
# # End Box CRUD
#
#
# @app.get("/contacts/", response_model=List[Contact])
# async def get_all_contacts():
#     user_count = await User.all().count()
#     print(f"Users are {user_count}")
#     return [
#         Contact(id='bdd2ddf2-3b93-4c0c-b3eb-da16a389c64b', email='j.feinauer@pragmaticminds.de', name='Julian Feinauer',
#                 picture='https://ca.slack-edge.com/T01BWJSLH9V-U01DL19HR6H-g799b8ba68f5-512',
#                 favorite_boxes=['a8f5e8ca-b55d-4f9e-9a98-145b62ad37b1']),
#         Contact(id='7b7f45ba-440f-496f-bd3e-b6c25ac6dde3', email='niklas@merz.de', name='Niklas Merz',
#                 picture='https://ca.slack-edge.com/T01BWJSLH9V-U01DGBU5TE2-9c36519a20c7-512',
#                 favorite_boxes=['a8f5e8ca-b55d-4f9e-9a98-145b62ad37b1', '2bc06d25-067c-493f-a32a-79bcc2ba88ff'])
#     ]
#
#
# #
# # @app.get("/boxes/all", response_model=List[Box])
# # async def get_all_boxes():
# #     return [
# #         Box(id='a8f5e8ca-b55d-4f9e-9a98-145b62ad37b1', label="Die Box in Kirchheim", address="Irgendwo in Kirchheim",
# #             lat=48.6355632, lon=9.4052465),
# #         Box(id='2bc06d25-067c-493f-a32a-79bcc2ba88ff', label="Die Box in Fulda", address="Irgendwo in Fulda",
# #             lat=50.4296862, lon=9.5423249),
# #     ]
#
#
# @app.post("/requests/new")
# async def new_request(send_request: SendRequest):
#     """
#     This endpoint is used when A wants to send something to B
#     :param send_request:
#     :return:
#     """
#     print(f'got send request: {send_request}')
#     requests.append(send_request)
#
#
# @app.post("/requests/sent/count/{user_id}", response_model=int)
# async def open_sent_requests_for_user(user_id: uuid.UUID):
#     """
#     Get Number of Open Sent Requetsts that wait for confirmation
#     :param user_id:
#     :return:
#     """
#     return len(requests)
#
#
# @app.get('/requests/{user_id}', response_model=List[SendRequest])
# async def get_open_requests(user_id: uuid.UUID):
#     """
#     Fetch all open Requets to given user
#     :param user_id:
#     :return:
#     """
#     response = [req for req in requests if req.receiver == user_id]
#     print(response)
#     return response
#
#
# @app.post("/responses/new")
# async def new_response(send_response: SendResponse):
#     pass
#
#
# @app.post("/responses/{user_id}", response_model=List[SendResponse])
# async def get_open_responses(user_id: uuid.UUID):
#     pass
#
#
# @app.post("/confirmations/{user_id}", response_model=List[ShipmentConfirmation])
# async def get_open_confirmations(user_id: uuid.UUID):
#     pass
#
#
# @app.get("/contacts", response_model=List[Contact])
# async def contacts():
#     pass
#
#
# @app.get("/shipment/{id}/delivery_code")
# async def get_delivery_code(id: uuid.UUID):
#     return "Hier dein Code"


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
