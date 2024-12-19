from fastapi import HTTPException, status
from service import user as user_service
from exceptions import NotFound


async def delete_user(user_id: str):
    try:
        await user_service.delete_user(user_id)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
