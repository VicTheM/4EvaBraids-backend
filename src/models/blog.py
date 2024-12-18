from models import PyObjectId
from models.comment import Comment
from pydantic import BaseModel, Field
from datetime import datetime
import datetime as dt


class BlogCreate(BaseModel):
    user_id: PyObjectId = Field(..., alias="user_id")
    thumbnail: str = Field(..., min_length=2, max_length=100)
    title: str = Field(..., min_length=2, max_length=50)
    body: str = Field(..., min_length=2, max_length=10000)


class Blog(BlogCreate):
    id: PyObjectId = Field(default=PyObjectId, alias="_id")
    preview: str = Field(..., min_length=2, max_length=100)
    likes: int = Field(default=0)
    comments: list[Comment] = Field(default_factory=list)
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )

    class Config:
        orm_mode = True


class BlogOut(Blog):
    class Config:
        orm_mode = True
        fields = {"body": {"exclude": True}}

    pass


class FullBlogOut(Blog):
    class Config:
        orm_mode = True

    pass
