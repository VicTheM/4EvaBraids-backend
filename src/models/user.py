from datetime import datetime
import datetime as dt
from models import PyObjectId
from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(
        ..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    phone_number: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=6, max_length=50)


class User(UserCreate):
    id: PyObjectId = Field(default=PyObjectId, alias="_id")
    hashed_password: str = Field(..., min_length=6, max_length=50)
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )

    class Config:
        orm_mode = True
        fields = {"password": {"exclude": True}}


class UserOut(User):
    class Config:
        orm_mode = True
        fields = {"hashed_password": {"exclude": True}}

    pass
