from typing import Annotated

from bson import ObjectId
from data.user import UserRepository
from exceptions import AlreadyExists, NotFound
from models import ObjectIdPydanticAnnotation
from models.user import UserInDB, UserCreate, UserOut

user_repo = UserRepository()


async def create_user(user: UserCreate) -> UserInDB:
    if await user_repo.get_user_by_email(
        user.email
    ) or await user_repo.get_user_by_phone_number(user.phone_number):
        raise AlreadyExists(
            "User with this email or phone number already exists"
        )
    return await user_repo.create_user(user)


async def get_all_users() -> list[UserInDB]:
    return await user_repo.get_all_users()


async def get_user_by_id(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> UserInDB:
    user = await user_repo.get_user_by_id(user_id)
    if user:
        return user
    raise NotFound(f"User with id {user_id} not found")


async def get_user_by_phone_number(phone_number: str) -> UserInDB:
    user = await user_repo.get_user_by_phone_number(phone_number)
    if user:
        return user
    raise NotFound(f"User with phone number {phone_number} not found")


async def get_user_by_email(email: str) -> UserInDB:
    user = await user_repo.get_user_by_email(email)
    if user:
        return user
    raise NotFound(f"User with email {email} not found")


async def update_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation], user: UserCreate
) -> UserInDB:
    user_got = await get_user_by_id(user_id)
    print(user_got)
    user_dict = user.model_dump()
    user_got.update(user_dict)
    del user_got["password"]
    return await user_repo.update_user(user_got)


async def delete_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> UserInDB:
    return await user_repo.delete_user(user_id)
