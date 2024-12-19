"""
User repository
"""

from typing import Annotated
from bson import ObjectId
from data import async_db
from models.user import UserInDB, UserCreate
from models import ObjectIdPydanticAnnotation
from utils import hash_password


class UserRepository:
    """
    User repository class
    """

    async def create_user(self, user: UserCreate) -> UserInDB:
        """
        Create a new user in the database

        Args:
            user (UserCreate): UserCreate model

        Returns:
            UserInDB: UserInDB model
        """
        user_dict = user.model_dump()
        user_dict["hashed_password"] = hash_password(user_dict["password"])
        del user_dict["password"]
        create_res = await async_db.users.insert_one(user_dict)
        return await self.get_user_by_id(create_res.inserted_id)

    async def get_all_users(self) -> list[UserInDB]:
        """
        Get all users from the database

        Returns:
            list[UserInDB]: List of UserInDB models
        """
        users = await async_db.users.find().to_list(1000)
        return users

    async def get_user_by_id(
        self, user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    ) -> UserInDB:
        """
        Get a user by id

        Args:
            user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): User id

        Returns:
            UserInDB: UserInDB model
        """
        user = await async_db.users.find_one({"_id": user_id})
        return user

    async def get_user_by_phone_number(self, phone_number: str) -> UserInDB:
        """
        Get a user by phone number

        Args:
            phone_number (str): Phone number

        Returns:
            UserInDB: UserInDB model
        """
        user = await async_db.users.find_one({"phone_number": phone_number})
        return user

    async def get_user_by_email(self, email: str) -> UserInDB:
        """
        Get a user by email

        Args:
            email (str): Email

        Returns:
            UserInDB: UserInDB model
        """
        user = await async_db.users.find_one({"email": email})
        return user

    async def update_user(self, user: UserInDB) -> UserInDB:
        """
        Update a user

        Args:
            user (UserInDB): UserInDB model

        Returns:
            UserInDB: UserInDB model
        """
        await async_db.users.update_one({"_id": user["_id"]}, {"$set": user})
        return user

    async def delete_user(
        self, user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    ) -> None:
        """
        Delete a user

        Args:
            user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): User id
        """
        await async_db.users.delete_one({"_id": user_id})
