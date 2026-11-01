import os
from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

# Register the student table before creating tables from Base.metadata.
from student.models import student as _student_model
from student.models.base import Base


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


def get_db(request: Request) -> Generator[Session, None, None]:
    engine: Engine | None = getattr(request.app.state, "engine", None)
    if engine is None:
        raise RuntimeError("The database engine has not been initialized.")

    with Session(engine) as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_db)]
