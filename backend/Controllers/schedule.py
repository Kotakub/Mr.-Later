import json
import fastapi

from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware  # Для CORS
from DTO.lessonDTO import LessonDTO
from Entity.lesson import lesson

router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.post("/add_lesson")
async def post_lesson(request: Request):
    json_data = await request.json()
    Lesson = lesson(json_data)
    Lesson.save_to_db()
    return {"received_json": Lesson}


@router.get("/")
async def get_schedule(request: Request):
    json_data = await request.json()
    return {"received_json": json_data}
