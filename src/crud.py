from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.vacancies.schemas import VacancyRead, VacancyCreate
from src.vacancies import models as vacancies_models
from src.auth import models as auth_models
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound, SQLAlchemyError


async def delete_self_user(db: AsyncSession, user_id: int):
    # Fetch the user instance
    result = await db.execute(select(auth_models.User).where(auth_models.User.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()


async def list_users(db: AsyncSession, limit: int = 100):
    result = await db.execute(select(auth_models.User).limit(limit))
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(auth_models.User).where(auth_models.User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(auth_models.User).where(auth_models.User.email == email))
    return result.scalar_one_or_none()


async def create_vacancy(new_vacancy_data: VacancyCreate, db: AsyncSession, user_id: int):
    new_vacancy = vacancies_models.Vacancy(**new_vacancy_data.dict())
    new_vacancy.user_id = user_id
    db.add(new_vacancy)
    await db.commit()
    await db.refresh(new_vacancy)
    return new_vacancy


async def delete_vacancy(vacancy_id: int, db: AsyncSession):
    try:
        row = await db.execute(
            select(vacancies_models.Vacancy).where(vacancies_models.Vacancy.id == vacancy_id)
        )
        vacancy = row.scalar_one()

        await db.delete(vacancy)
        await db.commit()

        return {"message": f"Successfully deleted Vacancy with id {vacancy_id}"}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Vacancy not found.")

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


async def get_vacancy(vacancy_id: int, db: AsyncSession):
    vacancy = await db.execute(select(vacancies_models.Vacancy).where(vacancies_models.Vacancy.id == int(vacancy_id)))
    return vacancy


async def list_vacancies(db: AsyncSession, limit: int = 100):
    result = await db.execute(select(vacancies_models.Vacancy).limit(limit))
    return result.scalars().all()
