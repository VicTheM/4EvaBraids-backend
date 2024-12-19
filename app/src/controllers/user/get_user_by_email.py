from fastapi import HTTPException, status
from service import user as user_service
from models.user import UserOut
from exceptions import NotFound


async def get_user_by_email(email: str) -> UserOut:
    try:
        user = await user_service.get_user_by_email(email)
        return user
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
