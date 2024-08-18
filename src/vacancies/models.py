from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Vacancy(Base):
    __tablename__ = "vacancy"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    salary = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="vacancies")

    def __repr__(self) -> str:
        return f"Vacancy (id={self.id!r}, employer={self.user_id.name!r}, title={self.title!r}, description={self.description!r})"
