from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from datetime import date, time, timedelta
from database_ORM import *
from database_main import get_async_session
from Router_Auth import get_current_user_db
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
async def post_lesson(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user_db),
):
    try:
        # Получаем JSON из тела запроса
        json_data = await request.json()

        # Проверяем, что пользователь добавляет урок себе
        if json_data["user_login"] != current_user.login:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only add lessons to your own schedule",
            )

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

        # TODO current.user

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

        # TODO убрать
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
    lesson_id: int,
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user_db),
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

        if lesson.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own lessons",
            )

        repeat_types = ["weekly", "biweekly", "none"]
        week = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

        # for u in session.query(User).all():
        #     print (u.__dict__)
        # Подготавливаем данные для обновления
        update_data = {}
        if "teacher_name" in json_data:
            update_data["teacher_name"] = f'{json_data["teacher_name"]}'
        if "subject_name" in json_data:
            update_data["subject_name"] = f'{json_data["subject_name"]}'

        if "startDate" in json_data:
            try:
                tmp_date = date.fromisoformat(json_data["startDate"])
                if tmp_date.year > 2300:
                    tmp_date.year = 2300
                update_data["startDate"] = tmp_date
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect startDate",
                )
        if "endDate" in json_data:
            try:
                tmp_date = date.fromisoformat(json_data["endDate"])
                if tmp_date.year > 2300:
                    tmp_date.year = 2300
                update_data["endDate"] = tmp_date
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect startDate",
                )

        if "startTime" in json_data:
            try:
                update_data["startTime"] = time.fromisoformat(json_data["startTime"])
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect startTime",
                )
        if "endTime" in json_data:
            try:
                update_data["endTime"] = time.fromisoformat(json_data["endTime"])
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect endTime",
                )

        if "repeat" in json_data:
            if json_data["repeat"] in repeat_types:
                update_data["repeat"] = f'{json_data["repeat"]}'
        if "dayOfWeek" in json_data:
            if json_data["dayOfWeek"] in week:
                update_data["dayOfWeek"] = f'{json_data["dayOfWeek"]}'

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

        # TODO убрать
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
        print("ОШИБКА ЭДИТ ЛЕССОН")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating lesson: {str(e)}",
        )


@router.delete("/delete_lesson/{lesson_id}")
async def delete_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user_db),
):
    try:
        # Проверяем существование урока и принадлежность пользователю
        lesson = await get_lessons_by_id(db, lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found"
            )

        if lesson.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own lessons",
            )

        # Удалаяем занятие
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


@router.put("/edit_comment")
async def edit_comment(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user_db),
):
    try:
        # Получаем JSON из тела запроса
        comment_data = await request.json()

        # Проверяем, что урок принадлежит пользователю
        lesson = await get_lessons_by_id(db, comment_data["lesson_id"])
        if not lesson or lesson.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit comments for your own lessons",
            )

        try:
            tmp_date = datetime.strptime(comment_data["lesson_date"], "%Y-%m-%d").date()
            if tmp_date.year > 2300:
                tmp_date.year = 2300
            comment_data["lesson_date"] = tmp_date
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect lesson_date",
            )
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
    # TODO посмотреть
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cant edit comment",
        )
    return


@router.patch("/save_schedule")
async def save_schedule(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user_db),
):
    try:
        # Получаем JSON из тела запроса
        save_data = await request.json()

        # Проверяем, что пользователь сохраняет расписание себе
        if save_data["my_login"] != current_user.login:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only save schedule to your own account",
            )

        user_me = await get_user_by_login(db, save_data["my_login"])
        user_save = await get_user_by_login(db, save_data["save_login"])

        if not user_save:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        delete_lessons = await get_lessons_by_user(db, user_me.id)
        if delete_lessons:
            for lesson in delete_lessons:
                await delete_lesson_by_id(db, lesson.id)

        save_lessons = await get_lessons_by_user(db, user_save.id)
        if not save_lessons:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lessons for save not found",
            )
        else:
            for lesson in save_lessons:
                lesson_data = {
                    "user_id": user_me.id,
                    "teacher_name": lesson.teacher_name,
                    "subject_name": lesson.subject_name,
                    "room": lesson.room,
                    "startDate": lesson.startDate,
                    "endDate": lesson.endDate,
                    "startTime": lesson.startTime,
                    "endTime": lesson.endTime,
                    "repeat": lesson.repeat,
                    "dayOfWeek": lesson.dayOfWeek,
                }
                await add_new_lesson(db, lesson_data)

        return {"message": "Schedule saved successfully"}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cant save schedule: {str(e)}",
        )
    return


@router.post("/attendance")
async def mark_attendance(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user_db),
):
    try:
        # Получаем JSON из тела запроса
        attendance_data = await request.json()

        # Проверяем, что урок принадлежит пользователю
        lesson = await get_lessons_by_id(db, attendance_data["lesson_id"])
        if not lesson or lesson.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only mark attendance for your own lessons",
            )

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
