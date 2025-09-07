import json
import fastapi
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

# Импортируем роутеры
from Controllers import auth, schedule

app = FastAPI(redirect_slashes=False)

# Включаем роутеры
app.include_router(schedule.router)
app.include_router(auth.router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Main page"}


# Если нужно защитить роуты в app.py, импортируйте зависимости из auth
@app.get("/protected")
async def protected_route(current_user=Depends(auth.get_current_user_db)):
    return {"message": "This is a protected route", "user": current_user}
