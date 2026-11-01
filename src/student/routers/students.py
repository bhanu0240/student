from fastapi import APIRouter, HTTPException, Response, status

from student.database import DatabaseSession
from student.schemas.student import Student, StudentResponse
from student.services import students as student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/", response_model=list[StudentResponse])
def read_students(db: DatabaseSession) -> list[StudentResponse]:
    students = student_service.get_students(db)
    return [StudentResponse.model_validate(student) for student in students]


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: DatabaseSession) -> StudentResponse:
    student = student_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse.model_validate(student)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: Student, db: DatabaseSession) -> StudentResponse:
    created_student = student_service.create_student(db, student)
    return StudentResponse.model_validate(created_student)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student: Student, db: DatabaseSession
) -> StudentResponse:
    updated_student = student_service.update_student(db, student_id, student)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse.model_validate(updated_student)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_student(student_id: int, db: DatabaseSession) -> Response:
    deleted = student_service.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
