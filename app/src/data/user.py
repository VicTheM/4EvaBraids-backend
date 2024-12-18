from typing import Annotated
from bson import ObjectId
from data import async_db
from models.user import UserInDB, UserCreate
from models import ObjectIdPydanticAnnotation


class UserRepository:
    async def create_user(self, user: UserCreate) -> UserInDB:
        user = UserInDB(**user.model_dump())
        user = await async_db.users.insert_one(user.model_dump())
        return user

    async def get_all_users(self) -> list[UserInDB]:
        users = await async_db.users.find().to_list(1000)
        return users

    async def get_user_by_id(
        self, user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    ) -> UserInDB:
        user = await async_db.users.find_one({"_id": user_id})
        return user

    async def get_user_by_phone_number(self, phone_number: str) -> UserInDB:
        user = await async_db.users.find_one({"phone_number": phone_number})
        return user

    async def get_user_by_email(self, email: str) -> UserInDB:
        user = await async_db.users.find_one({"email": email})
        return user

    async def update_user(self, user: UserInDB) -> UserInDB:
        user = await async_db.users.update_one(
            {"_id": user.id}, {"$set": user.model_dump()}
        )
        return user

    async def delete_user(
        self, user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    ) -> UserInDB:
        user = await async_db.users.delete_one({"_id": user_id})
        return user
