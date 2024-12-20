from pytest import fixture, raises
import pytest
import asyncio
from models.user import UserCreate
from models.user import UserInDB, UserCreate
from data.user import UserRepository
from data import async_db
from faker import Faker
import time
import os

os.environ["ENV"] = "test"

fake = Faker()

# Fixture to avoid closure of event loop
@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Create fake user data for every test
@fixture
def user_data():
    return UserCreate(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number()[:15],
        password=fake.password(),
    )

# Create a user in the database
@fixture
async def created_user(user_data: UserCreate):
    """
    Fixture to create a user in the database
    """
    user_repo = UserRepository()
    return await user_repo.create_user(user_data)


# TESTS

@pytest.mark.asyncio
async def test_get_all_users(user_data):
    user_repo = UserRepository()

    # Clean the database and add users
    await async_db.users.delete_many({})
    for _ in range(3):
        await user_repo.create_user(user_data)

    # Get all users
    users = await user_repo.get_all_users()

    # Assertions
    assert len(users) == 3
    for user in users:
        assert user["_id"]
        assert user["email"] == user_data.email


@pytest.mark.asyncio
async def test_create_user(user_data: UserCreate):
    """
    Test create user
    """
    user_repo = UserRepository()
    await async_db.users.delete_many({})
    user = await user_repo.create_user(user_data)
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


@pytest.mark.asyncio
async def test_get_user_by_id(created_user):
    """
    Test get user by ID
    """
    user_repo = UserRepository()

    # Fetch user by ID
    user = await user_repo.get_user_by_id(created_user["_id"])

    # Assertions
    assert user
    assert user["_id"] == created_user["_id"]
    assert user["email"] == created_user["email"]


@pytest.mark.asyncio
async def test_get_user_by_phone_number(created_user):
    """
    Test get user by phone number
    """
    user_repo = UserRepository()

    # Fetch user by phone number
    user = await user_repo.get_user_by_phone_number(created_user["phone_number"])

    # Assertions
    assert user
    assert user["_id"] == created_user["_id"]
    assert user["phone_number"] == created_user["phone_number"]


@pytest.mark.asyncio
async def test_get_user_by_email(created_user):
    """
    Test get user by email
    """
    user_repo = UserRepository()

    # Fetch user by email
    user = await user_repo.get_user_by_email(created_user["email"])

    # Assertions
    assert user
    assert user["_id"] == created_user["_id"]
    assert user["email"] == created_user["email"]


@pytest.mark.asyncio
async def test_update_user(created_user):
    """
    Test update user
    """
    user_repo = UserRepository()

    # Modify the user and update
    created_user["first_name"] = "UpdatedName"
    # await asyncio.sleep(5)
    updated_user = await user_repo.update_user(created_user)

    # Assertions
    assert updated_user["first_name"] == "UpdatedName"

    # print(f"Previous Time {created_user['date_created']}")
    # print(f"Updated Time {updated_user['date_updated']}")


@pytest.mark.asyncio
async def test_delete_user(created_user):
    """
    Test delete user
    """
    user_repo = UserRepository()

    await user_repo.delete_user(created_user["_id"])
    user = await user_repo.get_user_by_id(created_user["_id"])
    assert user is None

