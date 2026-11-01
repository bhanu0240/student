from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from student.models.base import Base


class Student(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0)
    grade: str = Field(min_length=1, max_length=20)


class StudentResponse(Student):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StudentRecord(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    grade: Mapped[str] = mapped_column(String(20), nullable=False)
