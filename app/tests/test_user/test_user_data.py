from pytest import fixture, raises
import pytest
from models.user import UserCreate
from models.user import UserInDB, UserCreate
import os

os.environ["ENV"] = "test"
from data import async_db
from data.user import UserRepository
from faker import Faker
import datetime as dt

fake = Faker()


# Create fake user data for every test
@fixture
async def user_data():
    """
    Fixture to create fake user data

    Returns:
        UserCreate: UserCreate model
    """
    await async_db.users.delete_many({})
    yield UserCreate(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number()[:15],
        password=fake.password(),
    )
    await async_db.users.delete_many({})


# Create a user in the database
@fixture
async def created_user(user_data: UserCreate):
    """
    Fixture to create a user in the database

    Args:
        user_data (UserCreate): UserCreate model
    """
    await async_db.users.delete_many({})
    user_repo = UserRepository()
    yield await user_repo.create_user(user_data)
    await async_db.users.delete_many({})


# TESTS


@pytest.mark.anyio
async def test_create_user(user_data: UserCreate):
    """
    Test create user

    Args:
        user_data (UserCreate): UserCreate model
    """
    user_repo = UserRepository()
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


@pytest.mark.anyio
async def test_get_all_users(user_data):
    """
    Test get all users

    Args:
        user_data (UserCreate): UserCreate model
    """
    user_repo = UserRepository()
    for _ in range(3):
        await user_repo.create_user(user_data)

    # Get all users
    users = await user_repo.get_all_users()

    # Assertions
    assert len(users) == 3
    for user in users:
        assert user["_id"]
        assert user["email"] == user_data.email


@pytest.mark.anyio
async def test_get_user_by_id(created_user):
    """
    Test get user by ID

    Args:
        created_user (UserInDB): UserInDB model
    """
    user_repo = UserRepository()

    # Fetch user by ID
    user = await user_repo.get_user_by_id(created_user["_id"])

    # Assertions
    assert user
    assert user["_id"] == created_user["_id"]
    assert user["email"] == created_user["email"]


@pytest.mark.anyio
async def test_get_user_by_phone_number(created_user):
    """
    Test get user by phone number

    Args:
        created_user (UserInDB): UserInDB model
    """
    user_repo = UserRepository()

    # Fetch user by phone number
    user = await user_repo.get_user_by_phone_number(
        created_user["phone_number"]
    )

    # Assertions
    assert user
    assert user["_id"] == created_user["_id"]
    assert user["phone_number"] == created_user["phone_number"]


@pytest.mark.anyio
async def test_get_user_by_email(created_user):
    """
    Test get user by email

    Args:
        created_user (UserInDB): UserInDB model
    """
    user_repo = UserRepository()

    # Fetch user by email
    user = await user_repo.get_user_by_email(created_user["email"])

    # Assertions
    assert user
    assert user["_id"] == created_user["_id"]
    assert user["email"] == created_user["email"]


@pytest.mark.anyio
async def test_update_user(created_user):
    """
    Test update user

    Args:
        created_user (UserInDB): UserInDB model
    """
    user_repo = UserRepository()

    # Modify the user and update
    created_user["first_name"] = "UpdatedName"
    initial_date_updated = created_user["date_updated"].replace(
        tzinfo=dt.timezone.utc
    )
    updated_user = await user_repo.update_user(created_user)

    # Assertions
    assert updated_user["first_name"] == "UpdatedName"
    assert updated_user["date_updated"] > initial_date_updated


@pytest.mark.anyio
async def test_delete_user(created_user):
    """
    Test delete user

    Args:
        created_user (UserInDB): UserInDB model
    """
    user_repo = UserRepository()

    await user_repo.delete_user(created_user["_id"])
    user = await user_repo.get_user_by_id(created_user["_id"])
    assert user is None
