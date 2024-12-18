from typing import Annotated

from bson import ObjectId
from data.user import UserRepository
from models import ObjectIdPydanticAnnotation
from models.user import UserInDB, UserCreate, UserOut

user_repo = UserRepository()


async def create_user(user: UserCreate) -> UserInDB:
    return await user_repo.create_user(user)


async def get_all_users() -> list[UserInDB]:
    return await user_repo.get_all_users()


async def get_user_by_id(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> UserInDB:
    return await user_repo.get_user_by_id(user_id)


async def get_user_by_phone_number(phone_number: str) -> UserInDB:
    return await user_repo.get_user_by_phone_number(phone_number)


async def get_user_by_email(email: str) -> UserInDB:
    return await user_repo.get_user_by_email(email)


async def update_user(user: UserInDB) -> UserInDB:
    return await user_repo.update_user(user)


async def delete_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> UserInDB:
    return await user_repo.delete_user(user_id)
