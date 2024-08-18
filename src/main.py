from fastapi import Depends, FastAPI, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

import src.auth.base_config as auth_base_config
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.database import create_db_and_tables
from contextlib import asynccontextmanager
from src.database import get_async_session
from src import crud, utils
from src.vacancies import schemas as vacancies_schemas
from src.auth import schemas as auth_schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
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


@app.get("/")
async def root():
    return {"message": "Welcome to ProHired!"}


@app.get("/users/me", response_model=auth_schemas.UserRead)
async def about_me(db: AsyncSession = Depends(get_async_session),
                   user_id: int = Depends(utils.get_user_id_from_cookies)):
    return await crud.get_user_by_id(db, user_id)


@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_async_session), limit: int = 100):
    users = await crud.list_users(db, limit)
    return users


@app.post("/vacancies/")
async def create_vacancy(new_vacancy_data: vacancies_schemas.VacancyCreate,
                         db: AsyncSession = Depends(get_async_session)):
    new_vacancy = await crud.create_vacancy(new_vacancy_data, db)
    return new_vacancy


@app.get("/vacancies/")
async def list_vacancies(db: AsyncSession = Depends(get_async_session), limit: int = 100):
    vacancies = await crud.list_vacancies(db, limit)
    return vacancies
