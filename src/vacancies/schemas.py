from pydantic import BaseModel


class VacancyRead(BaseModel):
    title: str
    salary: str
    description: str
    user_id: int

    class Config:
        from_attributes = True


class VacancyCreate(BaseModel):
    title: str
    salary: str
    description: str
    user_id: int

    class Config:
        from_attributes = True
