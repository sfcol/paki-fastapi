from tortoise.contrib.test import TestCase

from models import User


def test_something():
    print("Hallo")

class TestSomething(TestCase):

    def test_simple(self):
        user = User(name="Julian")
        user.save()

        copy = User.get(user.id)

        self.assertEqual(user, copy)

    # def test_create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    #     print("Hallo")
    #     response = client.post("/users", json={"username": "admin"})
    #     assert response.status_code == 200, response.text
    #     data = response.json()
    #     assert data["username"] == "admin"
    #     assert "id" in data
    #     user_id = data["id"]
    #
    #     async def get_user_by_db():
    #         user = await User.get(id=user_id)
    #         return user
    #
    #     user_obj = event_loop.run_until_complete(get_user_by_db())
    #     assert user_obj.id == user_id
