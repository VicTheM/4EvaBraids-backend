from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
import service.user as user_service
from models import ObjectIdPydanticAnnotation
from models.user import UserInDB, UserCreate, UserOut
from typing import Annotated, List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    user = await user_service.create_user(user)
    return user


@router.get("", response_model=List[UserOut])
@router.get("/", response_model=List[UserOut])
async def get_all_users():
    users = await user_service.get_all_users()
    return users


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
):
    user = await user_service.get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )


@router.get("/phone/{phone_number}", response_model=UserOut)
async def get_user_by_phone_number(phone_number: str):
    user = await user_service.get_user_by_phone_number(phone_number)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )


@router.get("/email/{email}", response_model=UserOut)
async def get_user_by_email(email: str):
    user = await user_service.get_user_by_email(email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation], user: UserInDB
):
    user = await user_service.update_user(user)
    return user


@router.delete("/{user_id}", response_model=UserOut)
async def delete_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
):
    user = await user_service.delete_user(user_id)
    return user
