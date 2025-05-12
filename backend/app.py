import json
import fastapi

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # Для CORS
from DTO.LessonDTO import LessonDTO

app = FastAPI()

# Разрешить запросы от Vue (иначе будет CORS-ошибка)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add_lesson")
async def post_lesson(request: Request):
    json_data = await request.json()
    Lesson = LessonDTO(json_data)
    return {"received_json": Lesson}
