from tortoise import Model, fields, Tortoise, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import CASCADE


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)


User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)


# Box Model

class Box(Model):
    id = fields.UUIDField(pk=True)
    label = fields.CharField(max_length=255)
    address = fields.CharField(max_length=255)
    lat = fields.DecimalField(decimal_places=6, max_digits=9)
    lon = fields.DecimalField(decimal_places=6, max_digits=9)


Box_Pydantic = pydantic_model_creator(Box, name="Box")
BoxIn_Pydantic = pydantic_model_creator(Box, name="BoxIn", exclude_readonly=True)


class Delivery(Model):
    id = fields.UUIDField(pk=True)
    sender = fields.ForeignKeyField("models.User", "deliveries_as_sender", on_delete=CASCADE, null=False)
    receiver = fields.ForeignKeyField("models.User", "deliveries_as_receiver", on_delete=CASCADE, null=False)


Delivery_Pydantic = pydantic_model_creator(Delivery, name="Delivery")
DeliveryIn_Pydantic = pydantic_model_creator(Delivery, name="DeliveryIn", exclude_readonly=True)


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['__main__']}
    )

    await Tortoise.generate_schemas()


async def do_something():
    # tournament = Tournament(name='my tourn')
    print("Start Storing...")
    # await tournament.save()
    print("Stored!")


async def main():
    await init()
    await do_something()


if __name__ == "__main__":
    print("Starting...")
    run_async(main())
    print("Finished...")
