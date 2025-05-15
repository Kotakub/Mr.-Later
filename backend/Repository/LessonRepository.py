import json
import datetime
import sqlite3
import os
from datetime import date, time
from typing import List, Dict, Any

db_path = os.path.join(os.path.dirname(__file__), "..", "..", "my_database.db")


class LessonRepository:
    def __init__(self, db_path: str = db_path):
        self.db_path = db_path

    def get_all(self) -> List[Dict[str, Any]]:
        """Получить все уроки из базы данных"""
        lessons = []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 
                    id, schedule_id, subject_name, 
                    startDate, endDate, startTime, endTime, 
                    repeat, dayOfWeek, teacher_name
                FROM lesson
            """
            )

            for row in cursor.fetchall():
                lesson = dict(row)
                # Конвертируем даты и время из строк в объекты
                lesson["startDate"] = date.fromisoformat(lesson["startDate"])
                lesson["endDate"] = date.fromisoformat(lesson["endDate"])
                lesson["startTime"] = time.fromisoformat(lesson["startTime"])
                lesson["endTime"] = time.fromisoformat(lesson["endTime"])
                lessons.append(lesson)

        return lessons

    def get_by_id(self, lesson_id: int) -> Dict[str, Any]:
        """Получить урок по ID"""
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
                return lesson
            return None

    def add_lesson(self, lesson_data: Dict[str, Any]) -> int:
        # Добавить новый урок
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

    def update_lesson(self, lesson_id: int, lesson_data: Dict[str, Any]) -> bool:
        """Обновить данные урока"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE lesson SET
                    schedule_id = ?,
                    subject_name = ?,
                    startDate = ?,
                    endDate = ?,
                    startTime = ?,
                    endTime = ?,
                    repeat = ?,
                    dayOfWeek = ?,
                    teacher_name = ?
                WHERE id = ?
            """,
                (
                    lesson_id,
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
            return cursor.rowcount > 0

    def delete_lesson(self, lesson_id: int) -> bool:
        """Удалить урок по ID"""
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
        """Получить все уроки для указанного расписания"""
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
