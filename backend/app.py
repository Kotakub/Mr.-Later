import json
import fastapi

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # Для CORS
from Controllers import auth, schedule

app = FastAPI(redirect_slashes=False)  # отключает автоматические редиректы для слэшей)

app.include_router(schedule.router)
# Разрешить запросы от Vue (иначе будет CORS-ошибка)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Main page"}
