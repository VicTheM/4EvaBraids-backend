from fastapi import HTTPException
from pytest import fixture, raises
import pytest
from models.user import UserCreate, UserOut
from httpx import AsyncClient, ASGITransport
import os

os.environ["ENV"] = "test"
from web.user import router as user_router
from web.auth import router as auth_router
from faker import Faker
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
    async with AsyncClient(
        transport=ASGITransport(user_router), base_url="http://test"
    ) as ac:
        response = await ac.post("/users/", json=user_data.model_dump())
        created_user = UserOut(**response.json())
        yield created_user
        await ac.delete(f"/users/{created_user.id}")
        await ac.aclose()


@fixture
async def created_user2(user_data2: UserCreate):
    """
    Fixture to create a user in the database

    Args:
        user_data (UserCreate): UserCreate model
    """
    async with AsyncClient(
        transport=ASGITransport(user_router), base_url="http://test"
    ) as ac:
        response = await ac.post("/users/", json=user_data2.model_dump())
        created_user = UserOut(**response.json())
        yield created_user
        await ac.delete(f"/users/{created_user.id}")
        await ac.aclose()


@pytest.mark.anyio
async def test_create_user(user_data: UserCreate):
    async with AsyncClient(
        transport=ASGITransport(user_router), base_url="http://test"
    ) as ac:
        response = await ac.post("/users/", json=user_data.model_dump())
        assert response.status_code == 201
        created_user = UserOut(**response.json())
        assert created_user
        assert created_user.id
        assert created_user.first_name == user_data.first_name
        assert created_user.last_name == user_data.last_name
        assert created_user.email == user_data.email
        assert created_user.phone_number == user_data.phone_number
        assert created_user.date_created
        assert created_user.date_updated
        await ac.delete(f"/users/{created_user.id}")
        await ac.aclose()


@pytest.mark.anyio
async def test_create_user_email_already_exists(
    created_user: UserOut, user_data2: UserCreate
):
    async with AsyncClient(
        transport=ASGITransport(user_router), base_url="http://test"
    ) as ac:
        user_data2.email = created_user.email
        with raises(Exception) as e:
            await ac.post("/users/", json=user_data2.model_dump())
        assert isinstance(e.value, HTTPException)
        assert e.value.status_code == 400
        assert (
            e.value.detail
            == "User with this email or phone number already exists"
        )
        await ac.aclose()


@pytest.mark.anyio
async def test_create_user_phone_number_already_exists(
    created_user: UserOut, user_data2: UserCreate
):
    async with AsyncClient(
        transport=ASGITransport(user_router), base_url="http://test"
    ) as ac:
        user_data2.phone_number = created_user.phone_number
        with raises(Exception) as e:
            await ac.post("/users/", json=user_data2.model_dump())
        assert isinstance(e.value, HTTPException)
        assert e.value.status_code == 400
        assert (
            e.value.detail
            == "User with this email or phone number already exists"
        )
        await ac.aclose()


@pytest.mark.anyio
async def test_get_all_users(user_data: UserCreate):
    async with AsyncClient(
        transport=ASGITransport(user_router), base_url="http://test"
    ) as ac:
        users_created = []
        for _ in range(3):
            user_data = UserCreate(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number=fake.phone_number()[:15],
                password=fake.password(),
            )
            user_res = await ac.post("/users/", json=user_data.model_dump())
            users_created.append(user_data.model_dump())
    async with AsyncClient(
        transport=ASGITransport(auth_router), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/token",
            data={
                "username": users_created[0]["email"],
                "password": users_created[0]["password"],
            },
        )
        print(response)
        token = response.json()["access_token"]
    response = await ac.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    users = [UserOut(**user) for user in response.json()]
    assert len(users) == 3
    for i in range(3):
        assert users[i].email == users_created[i]["email"]
    for user in users:
        await ac.delete(f"/users/{user.id}")
    await ac.aclose()
