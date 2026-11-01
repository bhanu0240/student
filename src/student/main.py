from fastapi import FastAPI

from student.database import lifespan
from student.routers.root import router as root_router
from student.routers.students import router as students_router

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
app.include_router(students_router)
