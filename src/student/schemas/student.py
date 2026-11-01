from pydantic import BaseModel, ConfigDict, Field


class Student(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0)
    grade: str = Field(min_length=1, max_length=20)


class StudentResponse(Student):
    id: int

    model_config = ConfigDict(from_attributes=True)
