from fastapi import HTTPException, status
from models.user import UserOut
from service import user as user_service


async def get_all_users() -> list[UserOut]:
    users = await user_service.get_all_users()
    return users
