from pydantic import BaseModel, Field


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
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "Software Engineer",
                "salary": "100000 USD",
                "description": "Develops software solutions."
            }
        }
