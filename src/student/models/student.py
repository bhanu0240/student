from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from student.models.base import Base


class StudentRecord(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    grade: Mapped[str] = mapped_column(String(20), nullable=False)
