from fastapi import Depends, FastAPI, HTTPException
from fastapi_users import FastAPIUsers

import src.auth.base_config as auth_base_config
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.database import create_db_and_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    print("Tables created!")
    yield


app = FastAPI(title="ProHired", lifespan=lifespan)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_base_config.auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_base_config.auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
