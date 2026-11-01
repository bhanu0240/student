from sqlalchemy import select
from sqlalchemy.orm import Session

from student.models.student import StudentRecord


def get_by_id(session: Session, student_id: int) -> StudentRecord | None:
    return session.get(StudentRecord, student_id)


def get_all(session: Session) -> list[StudentRecord]:
    return list(session.scalars(select(StudentRecord)).all())


def add(session: Session, student: StudentRecord) -> StudentRecord:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def save(session: Session, student: StudentRecord) -> StudentRecord:
    session.commit()
    session.refresh(student)
    return student


def delete(session: Session, student: StudentRecord) -> None:
    session.delete(student)
    session.commit()
