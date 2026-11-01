import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from student.database import get_db
from student.models.base import Base
from student.models.student import Student, StudentRecord, StudentResponse


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
    )

    database_url: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    database_url = os.getenv("DATABASE_URL") or Settings().database_url
    engine = create_engine(database_url)
    try:
        Base.metadata.create_all(engine)
        app.state.engine = engine
        yield
    finally:
        engine.dispose()


app = FastAPI(lifespan=lifespan)
DatabaseSession = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student API!"}


@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: DatabaseSession) -> StudentResponse:
    student = db.get(StudentRecord, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse.model_validate(student)


@app.post("/students/", response_model=StudentResponse, status_code=201)
def create_student(student: Student, db: DatabaseSession) -> StudentResponse:
    db_student = StudentRecord(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return StudentResponse.model_validate(db_student)