from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from datetime import date, time, timedelta
from database_ORM import *
from database_main import get_async_session
from models import Lessons

router = APIRouter()


async def get_dates(startDate, endDate, repeat):
    dates = []
    current_date = startDate
    end_date = endDate

    while current_date <= end_date:
        dates.append(current_date.isoformat())
        if repeat == "weekly":
            current_date += timedelta(weeks=1)
        elif repeat == "biweekly":
            current_date += timedelta(weeks=2)
        else:
            break
    return dates


async def get_attendances(lesson_id: int, db: AsyncSession):
    attendances = []
    attendance_list = await get_attendance_by_lesson(db, lesson_id)
    if not attendance_list:
        return attendances

    for att in attendance_list:
        attendances.append(att.lesson_date.isoformat())

    return attendances


async def get_comments(db: AsyncSession, lesson_id: int):
    comments = await get_comments_by_lesson(db, lesson_id)
    comments_data = []
    for comment in comments:
        comments_data.append(
            {
                "lesson_id": comment.lesson_id,
                "lesson_date": comment.lesson_date.isoformat(),
                "text": comment.text,
            }
        )
    return comments_data


@router.get("/get_schedule/{user_login}")
async def get_schedule(user_login: str, db: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_login(db, user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    lessons = await get_lessons_by_user(db, user.id)

    lessons_data = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": [],
        "comments": [],
    }

    for lesson in lessons:
        dates = await get_dates(lesson.startDate, lesson.endDate, lesson.repeat)
        attendances = await get_attendances(lesson.id, db)
        comments = await get_comments(db, lesson.id)

        lessons_data["comments"].extend(comments)
        lessons_data[lesson.dayOfWeek].append(
            {
                "id": lesson.id,
                "user_id": lesson.user_id,
                "teacher_name": lesson.teacher_name,
                "subject_name": lesson.subject_name,
                "room": lesson.room,
                "startDate": lesson.startDate.isoformat(),
                "endDate": lesson.endDate.isoformat(),
                "startTime": lesson.startTime.isoformat(),
                "endTime": lesson.endTime.isoformat(),
                "repeat": lesson.repeat,
                "dayOfWeek": lesson.dayOfWeek,
                "dates": dates,
                "attendances": attendances,
            }
        )
    print(lessons_data)
    return lessons_data


@router.post("/add_lesson")
async def post_lesson(request: Request, db: AsyncSession = Depends(get_async_session)):
    try:
        # Получаем JSON из тела запроса
        json_data = await request.json()

        # Валидация обязательных полей
        required_fields = [
            "user_login",
            "teacher_name",
            "subject_name",
            "startDate",
            "endDate",
            "startTime",
            "endTime",
            "repeat",
            "dayOfWeek",
            "room",
        ]

        for field in required_fields:
            if field not in json_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Проверяем существование пользователя
        user = await get_user_by_login(db, json_data["user_login"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Преобразуем строки в date и time объекты
        lesson_data = {
            "user_id": user.id,
            "teacher_name": json_data["teacher_name"],
            "subject_name": json_data["subject_name"],
            "startDate": date.fromisoformat(json_data["startDate"]),
            "endDate": date.fromisoformat(json_data["endDate"]),
            "startTime": time.fromisoformat(json_data["startTime"]),
            "endTime": time.fromisoformat(json_data["endTime"]),
            "repeat": json_data["repeat"],
            "dayOfWeek": json_data["dayOfWeek"],
            "room": json_data["room"],
        }

        # Добавляем урок
        new_lesson = await add_new_lesson(db, lesson_data)

        # Возвращаем созданный урок
        return {
            "id": new_lesson.id,
            "user_id": new_lesson.user_id,
            "teacher_name": new_lesson.teacher_name,
            "subject_name": new_lesson.subject_name,
            "startDate": new_lesson.startDate.isoformat(),
            "endDate": new_lesson.endDate.isoformat(),
            "startTime": new_lesson.startTime.isoformat(),
            "endTime": new_lesson.endTime.isoformat(),
            "repeat": new_lesson.repeat,
            "dayOfWeek": new_lesson.dayOfWeek,
            "room": new_lesson.room,
            "message": "Lesson created successfully",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date/time format: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating lesson: {str(e)}",
        )


@router.put("/edit_lesson/{lesson_id}")
async def edit_lesson(
    lesson_id: int, request: Request, db: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем JSON из тела запроса
        json_data = await request.json()

        # Проверяем существование урока
        lesson = await get_lessons_by_id(db, lesson_id)

        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found"
            )

        # Подготавливаем данные для обновления
        update_data = {}
        if "teacher_name" in json_data:
            update_data["teacher_name"] = json_data["teacher_name"]
        if "subject_name" in json_data:
            update_data["subject_name"] = json_data["subject_name"]
        if "startDate" in json_data:
            update_data["startDate"] = date.fromisoformat(json_data["startDate"])
        if "endDate" in json_data:
            update_data["endDate"] = date.fromisoformat(json_data["endDate"])
        if "startTime" in json_data:
            update_data["startTime"] = time.fromisoformat(json_data["startTime"])
        if "endTime" in json_data:
            update_data["endTime"] = time.fromisoformat(json_data["endTime"])
        if "repeat" in json_data:
            update_data["repeat"] = json_data["repeat"]
        if "dayOfWeek" in json_data:
            update_data["dayOfWeek"] = json_data["dayOfWeek"]

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
            )

        # Обновляем урок
        await db.execute(
            update(Lessons).where(Lessons.id == lesson_id).values(**update_data)
        )
        await db.commit()

        # Получаем обновленный урок
        result = await db.execute(select(Lessons).where(Lessons.id == lesson_id))
        updated_lesson = result.scalar_one()

        return {
            "id": updated_lesson.id,
            "user_id": updated_lesson.user_id,
            "teacher_name": updated_lesson.teacher_name,
            "subject_name": updated_lesson.subject_name,
            "startDate": updated_lesson.startDate.isoformat(),
            "endDate": updated_lesson.endDate.isoformat(),
            "startTime": updated_lesson.startTime.isoformat(),
            "endTime": updated_lesson.endTime.isoformat(),
            "repeat": updated_lesson.repeat,
            "dayOfWeek": updated_lesson.dayOfWeek,
            "message": "Lesson updated successfully",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date/time format: {str(e)}",
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating lesson: {str(e)}",
        )


@router.put("/edit_comment")
async def edit_comment(request: Request, db: AsyncSession = Depends(get_async_session)):
    try:
        # Получаем JSON из тела запроса
        comment_data = await request.json()
        comment_data["lesson_date"] = datetime.strptime(
            comment_data["lesson_date"], "%Y-%m-%d"
        ).date()
        comment = await get_comments_by_lesson_and_date(
            db, comment_data["lesson_id"], comment_data["lesson_date"]
        )
        if not comment:
            await add_new_comment(db, comment_data)
        elif comment_data["text"]:
            await update_comment(db, comment_data)
        else:
            await delete_comment(
                db, comment_data["lesson_id"], comment_data["lesson_date"]
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cant edit comment",
        )
    return


@router.delete("/delete_lesson/{lesson_id}")
async def delete_lesson(lesson_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        success = await delete_lesson_by_id(db, lesson_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found"
            )

        return {"message": "Lesson deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting lesson: {str(e)}",
        )


@router.patch("/save_schedule")
async def save_schedule(
    request: Request, db: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем JSON из тела запроса
        save_data = await request.json()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cant save schedule",
        )
    return


@router.post("/attendance")
async def mark_attendance(
    request: Request, db: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем JSON из тела запроса
        attendance_data = await request.json()

        # Проверяем наличие обязательных полей
        if "lesson_id" not in attendance_data or "lesson_date" not in attendance_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: lesson_id or lesson_date",
            )

        # Преобразуем строку даты в объект date
        try:
            lesson_date = date.fromisoformat(attendance_data["lesson_date"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD",
            )

        # Получаем attendance запись
        attendance = await get_attendance_by_lesson_and_date(
            db, attendance_data["lesson_id"], lesson_date
        )

        if attendance:
            await delete_attendance_by_lesson_and_date(
                db, attendance_data["lesson_id"], lesson_date
            )
            return {"attended": False}
        else:
            await add_attendance_by_lesson_and_date(
                db, attendance_data["lesson_id"], lesson_date
            )
            return {"attended": True}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cant edit attendance: {str(e)}",
        )
