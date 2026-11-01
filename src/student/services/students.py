from sqlalchemy.orm import Session

from student.models.student import StudentRecord
from student.repositories import students as student_repository
from student.schemas.student import Student


def get_students(session: Session) -> list[StudentRecord]:
    return student_repository.get_all(session)


def get_student(session: Session, student_id: int) -> StudentRecord | None:
    return student_repository.get_by_id(session, student_id)


def create_student(session: Session, student: Student) -> StudentRecord:
    record = StudentRecord(**student.model_dump())
    return student_repository.add(session, record)


def update_student(
    session: Session, student_id: int, student: Student
) -> StudentRecord | None:
    record = student_repository.get_by_id(session, student_id)
    if record is None:
        return None

    record.name = student.name
    record.age = student.age
    record.grade = student.grade
    return student_repository.save(session, record)


def delete_student(session: Session, student_id: int) -> bool:
    record = student_repository.get_by_id(session, student_id)
    if record is None:
        return False

    student_repository.delete(session, record)
    return True
