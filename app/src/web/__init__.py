"""
This module is responsible for creating the FastAPI app instance and including the user router.
"""

from fastapi import FastAPI
from web.user import router as user_router
from web.auth import router as auth_router
from web.blog import router as blog_router
from web.booking import router as bookings_router
from web.stats import router as stats_router


def create_app() -> FastAPI:
    """
    Creates the FastAPI app instance and includes the user router.

    Returns:
        FastAPI: The FastAPI app instance.
    """
    app = FastAPI()
    app.router.prefix = "/api"
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(blog_router)
    app.include_router(bookings_router)
    app.include_router(stats_router)

    return app
