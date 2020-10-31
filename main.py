import uuid
from datetime import date
from enum import Enum
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from starlette.middleware.cors import CORSMiddleware

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


class Contact(BaseModel):
    id: uuid.UUID
    email: EmailStr
    name: str
    picture: str
    favorite_boxes: List[uuid.UUID]


class Box(BaseModel):
    id: uuid.UUID
    # Random "Name" of Station
    label: str
    address: str
    lat: float
    lon: float


class ShipmentSizes(str, Enum):
    S: 'S'
    M: 'M'
    L: 'L'
    XL: 'XL'


class DropoffStatus(str, Enum):
    ACCEPTED: 'accepted'
    DENIED: 'denied'


# Step 1
class SendRequest(BaseModel):
    """
    I want to drop you something off
    Sender -> Backend -> Receiver
    """
    id: uuid.UUID
    sender: EmailStr
    receiver: EmailStr
    box: uuid.UUID
    size: ShipmentSizes
    dropoff_date: date


# Step 2
class SendResponse(BaseModel):
    """
    I accept and will pick it up
    Receiver -> Backend
    """
    request: SendRequest
    status: DropoffStatus
    pickup_date: date


# Step 3
class ShipmentConfirmation(BaseModel):
    """
    You have a DEAL!
    Backend -> Sender
    Backend -> Receiver
    """
    sender: EmailStr
    receiver: EmailStr
    box: uuid.UUID
    size: ShipmentSizes
    dropoff_date: date
    pickup_date: date


requests = {}


@app.get("/contacts/", response_model=List[Contact])
async def get_all_contacts():
    return [
        Contact(id='bdd2ddf2-3b93-4c0c-b3eb-da16a389c64b', email='j.feinauer@pragmaticminds.de', name='Julian Feinauer',
                picture='https://ca.slack-edge.com/T01BWJSLH9V-U01DL19HR6H-g799b8ba68f5-512', favorite_boxes=[]),
        Contact(id='7b7f45ba-440f-496f-bd3e-b6c25ac6dde3', email='niklas@merz.de', name='Niklas Merz',
                picture='https://ca.slack-edge.com/T01BWJSLH9V-U01DGBU5TE2-9c36519a20c7-512', favorite_boxes=[])
    ]


@app.get("/boxes/all", response_model=List[Box])
async def get_all_boxes():
    return [
        Box(id=uuid.uuid4(), label="", address="", lat=1.0, lon=2.0),
        Box(id=uuid.uuid4(), label="2", address="", lat=1.0, lon=2.0),
    ]


@app.post("/boxes/new")
async def get_all_boxes(box: Box):
    print("Got a Box:")
    print(box)


@app.post("/requests/new")
async def new_request(send_request: SendRequest):
    pass


@app.get('/requests/{user_id}', response_model=List[SendRequest])
async def get_open_requests(user_id: uuid.UUID):
    """
    Fetch all open Requets to given user
    :param user_id:
    :return:
    """
    pass


@app.post("/responses/new")
async def new_response(send_response: SendResponse):
    pass


@app.post("/responses/{user_id}", response_model=List[SendResponse])
async def get_open_responses(user_id: uuid.UUID):
    pass


@app.post("/confirmations/{user_id}", response_model=List[ShipmentConfirmation])
async def get_open_confirmations(user_id: uuid.UUID):
    pass


@app.get("/contacts", response_model=List[Contact])
async def contacts():
    pass


@app.get("/shipment/{id}/delivery_code")
async def get_delivery_code(id: uuid.UUID):
    return "Hier dein Code"
