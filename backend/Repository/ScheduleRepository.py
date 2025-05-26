import json
import datetime
import sqlite3
import os
from datetime import date, time
from typing import List, Dict, Any
from DTO.LessonDTO import LessonDTO


class LessonRepository:
    def __init__(self):

        self.db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../my_database.db")
        )

    def get_by_id(self, lesson_id: int) -> LessonDTO:
        # Получисть lesson по id
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM lesson WHERE id = ?
            """,
                (lesson_id,),
            )

            row = cursor.fetchone()
            if row:
                lesson = dict(row)
                lesson["startDate"] = date.fromisoformat(lesson["startDate"])
                lesson["endDate"] = date.fromisoformat(lesson["endDate"])
                lesson["startTime"] = time.fromisoformat(lesson["startTime"])
                lesson["endTime"] = time.fromisoformat(lesson["endTime"])
                return LessonDTO(lesson)
            return None

    def add_lesson(self, lesson_dto: LessonDTO) -> int:

        lesson_data = lesson_dto.to_dict()
        # Добавить новый lesson
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO lesson (
                    schedule_id, subject_name, 
                    startDate, endDate, startTime, endTime, 
                    repeat, dayOfWeek, teacher_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    lesson_data["schedule_id"],
                    lesson_data["subject_name"],
                    lesson_data.get("teacher_name"),
                    lesson_data["startDate"].isoformat(),
                    lesson_data["endDate"].isoformat(),
                    lesson_data["startTime"].isoformat(),
                    lesson_data["endTime"].isoformat(),
                    lesson_data["repeat"],
                    lesson_data["dayOfWeek"],
                ),
            )

            conn.commit()
            return cursor.lastrowid

    def update_lesson(self, lesson_id: int, lesson_dto: LessonDTO) -> bool:

        lesson_data = lesson_dto.to_dict()
        # Обновить данные lesson
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE lesson SET
                    schedule_id = ?,
                    subject_name = ?,
                    teacher_name = ?
                    startDate = ?,
                    endDate = ?,
                    startTime = ?,
                    endTime = ?,
                    repeat = ?,
                    dayOfWeek = ?
                WHERE id = ?
            """,
                (
                    lesson_data["schedule_id"],
                    lesson_data["subject_name"],
                    lesson_data["teacher_name"],
                    lesson_data["startDate"].isoformat(),
                    lesson_data["endDate"].isoformat(),
                    lesson_data["startTime"].isoformat(),
                    lesson_data["endTime"].isoformat(),
                    lesson_data["repeat"],
                    lesson_data["dayOfWeek"],
                    lesson_id,
                ),
            )

            conn.commit()
            return cursor.rowcount > 0

    def delete_lesson(self, lesson_id: int) -> bool:
        # Удалить lesson по id
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM lesson WHERE id = ?
            """,
                (lesson_id,),
            )

            conn.commit()
            return cursor.rowcount > 0

    def get_lessons_by_schedule(self, schedule_id: int) -> List[Dict[str, Any]]:
        # Получить все уроки по schedule_id
        lessons = []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM lesson 
                WHERE schedule_id = ?
                ORDER BY dayOfWeek, startTime
            """,
                (schedule_id,),
            )

            for row in cursor.fetchall():
                lesson = dict(row)
                lesson["startDate"] = date.fromisoformat(lesson["startDate"])
                lesson["endDate"] = date.fromisoformat(lesson["endDate"])
                lesson["startTime"] = time.fromisoformat(lesson["startTime"])
                lesson["endTime"] = time.fromisoformat(lesson["endTime"])
                lessons.append(lesson)

        return lessons
