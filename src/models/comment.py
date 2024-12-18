from models import PyObjectId
from pydantic import BaseModel, Field
from datetime import datetime
import datetime as dt


class CommentCreate(BaseModel):
    user_id: PyObjectId = Field(..., alias="user_id")
    text: str = Field(..., min_length=2, max_length=1000)


class Comment(CommentCreate):
    id: PyObjectId = Field(default=PyObjectId, alias="_id")
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )

    class Config:
        orm_mode = True


class CommentOut(Comment):
    class Config:
        orm_mode = True

    pass
