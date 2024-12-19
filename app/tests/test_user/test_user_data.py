from pytest import fixture, raises
import pytest
import pytest_asyncio
from models.user import UserCreate
from models.user import UserInDB, UserCreate
from data.user import UserRepository
from data import async_db
from faker import Faker

fake = Faker()


@fixture
def user_data():
    return UserCreate(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number()[:15],
        password=fake.password(),
    )


@pytest.mark.asyncio
async def test_create_user(user_data: UserCreate):
    user_repo = UserRepository()
    await async_db.users.delete_many({})
    user = await user_repo.create_user(user_data)
    print(user)
    assert user
    assert user["_id"]
    assert user["first_name"] == user_data.first_name
    assert user["last_name"] == user_data.last_name
    assert user["email"] == user_data.email
    assert user["phone_number"] == user_data.phone_number
    assert user["date_created"]
    assert user["date_updated"]
    assert user["hashed_password"]
    with raises(Exception):
        assert user["password"] == user_data.password
