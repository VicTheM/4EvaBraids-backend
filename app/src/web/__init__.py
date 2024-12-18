from fastapi import FastAPI
from web.user import router as user_router


def create_app():
    app = FastAPI()
    app.router.prefix = "/api"
    app.include_router(user_router)
    return app
