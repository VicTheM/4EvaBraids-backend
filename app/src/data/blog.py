"""
Blog Repository
"""

from typing import Annotated
import datetime as dt
from datetime import datetime
from bson import ObjectId
from data import async_db
from models.blog import BlogInDB, BlogCreate
from models import ObjectIdPydanticAnnotation


class BlogRepository:
    """
    Blog repository class
    """

    async def create_blog(self, blog: BlogCreate) -> BlogInDB:
        """
        Create a new blog in the database

        Args:
            blog (BlogCreate): BlogCreate model

        Returns:
            BlogInDB: BlogInDB model
        """
        blog_dict = blog.model_dump()
        blog_dict["preview"] = blog_dict["body"][:100]
        blog_dict["date_created"] = datetime.now(dt.timezone.utc)
        blog_dict["date_updated"] = datetime.now(dt.timezone.utc)
        create_res = await async_db.blogs.insert_one(blog_dict)
        return await self.get_blog_by_id(create_res.inserted_id)

    async def get_all_blogs(self) -> list[BlogInDB]:
        """
        Get all blogs from the database

        Returns:
            list[BlogInDB]: List of BlogInDB models
        """
        blogs = await async_db.blogs.find().to_list(1000)
        return blogs

    async def get_blog_by_id(
        self, blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    ) -> BlogInDB:
        """
        Get a blog by id

        Args:
            blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): Blog id

        Returns:
            BlogInDB: BlogInDB model
        """
        blog = await async_db.blogs.find_one({"_id": ObjectId(blog_id)})
        return blog

    async def update_blog(
        self,
        blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
        blog: BlogCreate,
    ) -> BlogInDB:
        """
        Update a blog in the database

        Args:
            blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): Blog id
            blog (BlogCreate): BlogCreate model

        Returns:
            BlogInDB: BlogInDB model
        """
        blog_dict = blog.model_dump()
        blog_dict["date_updated"] = datetime.now(dt.timezone.utc)
        update_res = await async_db.blogs.update_one(
            {"_id": ObjectId(blog_id)}, {"$set": blog_dict}
        )
        return await self.get_blog_by_id(blog_id)

    async def delete_blog(
        self, blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    ) -> bool:
        """
        Delete a blog from the database

        Args:
            blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): Blog id

        Returns:
            bool: True if blog is deleted
        """
        delete_res = await async_db.blogs.delete_one(
            {"_id": ObjectId(blog_id)}
        )
        return delete_res.deleted_count == 1
