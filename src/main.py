from fastapi import FastAPI, HTTPException, Cookie, Response, Depends
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
async def lifespan():
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


@app.delete("/users/")
async def delete_user(response: Response, db: AsyncSession = Depends(get_async_session),
                      user_id: int = Depends(utils.get_user_id_from_cookies)):
    await crud.delete_self_user(db, user_id)
    response.delete_cookie(key="usersAuth")
    return {"message": "User and their vacancies deleted successfully."}


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
                         db: AsyncSession = Depends(get_async_session),
                         user_id: int = Depends(utils.get_user_id_from_cookies)):
    print(new_vacancy_data)
    new_vacancy = await crud.create_vacancy(new_vacancy_data, db, user_id)
    return new_vacancy


@app.get("/vacancies/{vacancy_id}", response_model=vacancies_schemas.VacancyRead)
async def get_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_async_session)):
    vacancy = await crud.get_vacancy(vacancy_id, db)
    return vacancy


@app.delete("/vacancies/{vacancy_id}")
async def delete_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_async_session), ):
    vacancy = await crud.delete_vacancy(vacancy_id, db)
    return vacancy


@app.get("/vacancies/")
async def list_vacancies(db: AsyncSession = Depends(get_async_session), limit: int = 100):
    vacancies = await crud.list_vacancies(db, limit)
    return vacancies
