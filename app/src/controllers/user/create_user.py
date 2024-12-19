from fastapi import HTTPException, status
from service import user as user_service
from models.user import UserCreate
from exceptions import AlreadyExists


async def create_user(user: UserCreate):
    try:
        user = await user_service.create_user(user)
        return user
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )
