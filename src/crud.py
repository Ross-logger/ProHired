from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.vacancies.schemas import VacancyRead, VacancyCreate
from src.vacancies import models as vacancies_models
from src.auth import models as auth_models
from src import utils


async def list_users(db: AsyncSession, limit: int = 100):
    result = await db.execute(select(auth_models.User).limit(limit))
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(auth_models.User).where(auth_models.User.id == int(user_id)))
    return result.scalar_one_or_none()



async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(auth_models.User).where(auth_models.User.email == email))
    return result.scalar_one_or_none()


async def create_vacancy(new_vacancy_data: VacancyCreate, db: AsyncSession):
    print("New vacancy data: ", new_vacancy_data.dict())
    new_vacancy = vacancies_models.Vacancy(**new_vacancy_data.dict())
    db.add(new_vacancy)
    await db.commit()
    await db.refresh(new_vacancy)
    return new_vacancy


async def list_vacancies(db: AsyncSession, limit: int = 100):
    result = await db.execute(select(vacancies_models.Vacancy).limit(limit))
    return result.scalars().all()
