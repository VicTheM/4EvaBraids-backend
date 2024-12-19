"""
User service module
"""

from typing import Annotated
from bson import ObjectId
from data.user import UserRepository
from exceptions import AlreadyExists, NotFound
from models import ObjectIdPydanticAnnotation
from models.user import UserInDB, UserCreate, UserOut

user_repo = UserRepository()


async def create_user(user: UserCreate) -> UserOut:
    """
    Create a new user in the database

    Args:
        user (UserCreate): UserCreate model

    Returns:
        UserInDB: UserInDB model
    """
    if await user_repo.get_user_by_email(
        user.email
    ) or await user_repo.get_user_by_phone_number(user.phone_number):
        raise AlreadyExists(
            "User with this email or phone number already exists"
        )
    return UserOut(**(await user_repo.create_user(user)))


async def get_all_users() -> list[UserOut]:
    """
    Get all users from the database

    Returns:
        list[UserInDB]: List of UserInDB models
    """
    return [UserOut(**user) for user in await user_repo.get_all_users()]


async def get_user_by_id(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> UserOut:
    """
    Get a user by id

    Args:
        user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): User id

    Returns:
        UserInDB: UserInDB model
    """
    user = await user_repo.get_user_by_id(user_id)
    if user:
        return UserOut(**user)
    raise NotFound(f"User with id {user_id} not found")


async def get_user_by_phone_number(phone_number: str) -> UserOut:
    """
    Get a user by phone number

    Args:
        phone_number (str): Phone number

    Returns:
        UserInDB: UserInDB model
    """
    user = await user_repo.get_user_by_phone_number(phone_number)
    if user:
        return UserOut(**user)
    raise NotFound(f"User with phone number {phone_number} not found")


async def get_user_by_email(email: str) -> UserOut:
    """
    Get a user by email

    Args:
        email (str): Email

    Returns:
        UserInDB: UserInDB model
    """
    user = await user_repo.get_user_by_email(email)
    if user:
        return UserOut(**user)
    raise NotFound(f"User with email {email} not found")


async def update_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation], user: UserCreate
) -> UserOut:
    """
    Update a user

    Args:
        user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): User id
        user (UserCreate): UserCreate model

    Returns:
        UserInDB: UserInDB model
    """
    user_got = await get_user_by_id(user_id)
    if not user_got:
        raise NotFound(f"User with id {user_id} not found")
    if user_got["email"] != user.email and await user_repo.get_user_by_email(
        user.email
    ):
        raise AlreadyExists("User with this email already exists")
    if user_got[
        "phone_number"
    ] != user.phone_number and await user_repo.get_user_by_phone_number(
        user.phone_number
    ):
        raise AlreadyExists("User with this phone number already exists")
    user_dict = user.model_dump()
    user_got.update(user_dict)
    del user_got["password"]
    return UserOut(**(await user_repo.update_user(user_got)))


async def delete_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> None:
    """
    Delete a user

    Args:
        user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): User id
    """
    user = await get_user_by_id(user_id)
    if not user:
        raise NotFound(f"User with id {user_id} not found")
    return await user_repo.delete_user(user_id)
