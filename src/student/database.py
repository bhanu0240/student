from collections.abc import Generator

from fastapi import Request
from sqlalchemy import Engine
from sqlalchemy.orm import Session


def get_db(request: Request) -> Generator[Session, None, None]:
    engine: Engine | None = getattr(request.app.state, "engine", None)
    if engine is None:
        raise RuntimeError("The database engine has not been initialized.")

    with Session(engine) as session:
        yield session
