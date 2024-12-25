from pytest import fixture, raises
import pytest
from models.user import UserCreate, UserOut
import os

os.environ["ENV"] = "test"
from service import user as user_service
from faker import Faker
from exceptions import AlreadyExists, NotFound
import datetime as dt

fake = Faker()


@fixture
async def user_data():
    """
    Fixture to create fake user data

    Returns:
        UserCreate: UserCreate model
    """
    yield UserCreate(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number()[:15],
        password=fake.password(),
    )


@fixture
async def user_data2():
    """
    Fixture to create fake user data

    Returns:
        UserCreate: UserCreate model
    """
    yield UserCreate(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number()[:15],
        password=fake.password(),
    )


@fixture
async def created_user(user_data: UserCreate):
    """
    Fixture to create a user in the database

    Args:
        user_data (UserCreate): UserCreate model
    """
    created_user = await user_service.create_user(user_data)
    yield created_user
    try:
        await user_service.delete_user(created_user.id)
    except NotFound:
        pass


@fixture
async def created_user2(user_data2: UserCreate):
    """
    Fixture to create a user in the database

    Args:
        user_data (UserCreate): UserCreate model
    """
    created_user = await user_service.create_user(user_data2)
    yield created_user
    try:
        await user_service.delete_user(created_user.id)
    except NotFound:
        pass


@pytest.mark.anyio
async def test_create_user(user_data: UserCreate):
    """
    Test create user

    Args:
        user_data (UserCreate): UserCreate model
    """
    created_user = await user_service.create_user(user_data)
    assert created_user.email == user_data.email
    await user_service.delete_user(created_user.id)


@pytest.mark.anyio
async def test_create_user_email_already_exists(
    user_data: UserCreate, created_user: UserOut
):
    """
    Test create user with email that already exists

    Args:
        created_user (UserCreate): UserCreate model
    """
    user_data.email = created_user.email
    with raises(AlreadyExists):
        await user_service.create_user(user_data)


@pytest.mark.anyio
async def test_create_user_phone_number_already_exists(
    user_data: UserCreate, created_user: UserOut
):
    """
    Test create user with phone number that already exists

    Args:
        created_user (UserCreate): UserCreate model
    """
    user_data.phone_number = created_user.phone_number
    with raises(AlreadyExists):
        await user_service.create_user(user_data)


@pytest.mark.anyio
async def test_get_all_users(user_data: UserCreate):
    """
    Test get all users

    Args:
        user_data (UserCreate): UserCreate model
    """
    await user_service.create_user(user_data)
    users = await user_service.get_all_users()
    assert len(users) > 0
    await user_service.delete_user(users[0].id)


@pytest.mark.anyio
async def test_get_user_by_id(created_user: UserOut):
    """
    Test get user by ID

    Args:
        created_user (UserCreate): UserCreate model
    """
    user = await user_service.get_user_by_id(created_user.id)
    assert user.id == created_user.id
    assert user.email == created_user.email


@pytest.mark.anyio
async def test_get_user_by_id_not_found():
    """
    Test get user by ID not found
    """
    with raises(NotFound):
        await user_service.get_user_by_id("60f790d0b3f4f7b6c2f2d2d4")


@pytest.mark.anyio
async def test_get_user_by_email(created_user: UserOut):
    """
    Test get user by email

    Args:
        created_user (UserCreate): UserCreate model
    """
    user = await user_service.get_user_by_email(created_user.email)
    assert user.id == created_user.id
    assert user.email == created_user.email


@pytest.mark.anyio
async def test_get_user_by_email_not_found():
    """
    Test get user by email not found
    """
    with raises(NotFound):
        await user_service.get_user_by_email("test@test.com")


@pytest.mark.anyio
async def test_get_user_by_phone_number(created_user: UserOut):
    """
    Test get user by phone number

    Args:
        created_user (UserCreate): UserCreate model
    """
    user = await user_service.get_user_by_phone_number(
        created_user.phone_number
    )
    assert user.id == created_user.id
    assert user.phone_number == created_user.phone_number


@pytest.mark.anyio
async def test_get_user_by_phone_number_not_found():
    """
    Test get user by phone number not found
    """
    with raises(NotFound):
        await user_service.get_user_by_phone_number("1234567890")


@pytest.mark.anyio
async def test_update_user(created_user: UserOut, user_data: UserCreate):
    """
    Test update user

    Args:
        created_user (UserCreate): UserCreate model
    """
    user = await user_service.update_user(created_user.id, user_data)
    assert user.email == user_data.email
    assert user.phone_number == user_data.phone_number


@pytest.mark.anyio
async def test_update_user_not_found(user_data: UserCreate):
    """
    Test update user not found

    Args:
        user_data (UserCreate): UserCreate model
    """
    with raises(NotFound):
        await user_service.update_user("60f790d0b3f4f7b6c2f2d2d4", user_data)


@pytest.mark.anyio
async def test_update_user_email_already_exists(
    created_user: UserOut, created_user2: UserOut, user_data: UserCreate
):
    """
    Test update user with email that already exists

    Args:
        created_user (UserCreate): UserCreate model
    """
    user_data.email = created_user2.email
    with raises(AlreadyExists):
        await user_service.update_user(created_user.id, user_data)


@pytest.mark.anyio
async def test_update_user_phone_number_already_exists(
    created_user: UserOut, created_user2: UserOut, user_data: UserCreate
):
    """
    Test update user with phone number that already exists

    Args:
        created_user (UserCreate): UserCreate model
    """
    user_data.phone_number = created_user2.phone_number
    with raises(AlreadyExists):
        await user_service.update_user(created_user.id, user_data)


@pytest.mark.anyio
async def test_delete_user(created_user: UserOut):
    """
    Test delete user

    Args:
        created_user (UserCreate): UserCreate model
    """
    await user_service.delete_user(created_user.id)
    with raises(NotFound):
        await user_service.get_user_by_id(created_user.id)


@pytest.mark.anyio
async def test_delete_user_not_found():
    """
    Test delete user not found
    """
    with raises(NotFound):
        await user_service.delete_user("60f790d0b3f4f7b6c2f2d2d4")
