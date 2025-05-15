import json
import datetime
import sqlite3
import os

from datetime import date, time

db_path = os.path.join(os.path.dirname(__file__), "..", "..", "my_database.db")


class lesson:
    def __init__(self, lesson_data: dict):

        # Переход из "year-month-day" в [year, month, day]
        startDate = [int(x) for x in (lesson_data["startDate"]).split("-")]
        endDate = [int(x) for x in (lesson_data["endDate"]).split("-")]

        # Переход из "hour:minute" в [hour, minute]
        startTime = [int(x) for x in (lesson_data["startTime"]).split(":")]
        endTime = [int(x) for x in (lesson_data["endTime"]).split(":")]

        # Добавление атрибутов класса
        self.lesson_id = lesson_data["lesson_id"]
        self.schedule_id = lesson_data["schedule_id"]
        self.subject_name = lesson_data["subject_name"]
        self.teacher_name = lesson_data["teacher_name"]
        self.startDate = date(startDate[0], startDate[1], startDate[2])
        self.endDate = date(endDate[0], endDate[1], endDate[2])
        self.startTime = time(startTime[0], startTime[1]).strftime("%H:%M:%S")
        self.endTime = time(endTime[0], endTime[1]).strftime("%H:%M:%S")
        self.repeat = lesson_data["repeat"]
        self.dayOfWeek = lesson_data["dayOfWeek"]

    # Строковый вывод
    def __str__(self):
        return (
            f"Lesson {self.lesson_id}: {self.subject_name} "
            f"with {self.teacher_name}\n"
            f"Date: {self.start_date} - {self.end_date}\n"
            f"Time: {self.start_time} - {self.end_time}"
        )

    # Перевод в словарь
    def to_dict(self) -> dict:
        return {
            "lesson_id": self.lesson_id,
            "schedule_id": self.schedule_id,
            "subject_name": self.subject_name,
            "teacher_name": self.teacher_name,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "startTime": self.start_time,
            "endTime": self.end_time,
        }

    def save_to_db(self):

        # Подключение к базе данных
        with sqlite3.connect(db_path) as conn:
            # Создание курсора
            cursor = conn.cursor()

            if not self.lesson_id:
                cursor.execute(
                    """
                INSERT INTO lesson(schedule_id, subject_name, teacher_name, startDate, endDate, startTime, endTime, repeat, dayOfWeek)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                    (
                        self.schedule_id,
                        self.subject_name,
                        self.teacher_name,
                        self.startDate,
                        self.endDate,
                        self.startTime,
                        self.endTime,
                        self.repeat,
                        self.dayOfWeek,
                    ),
                )
            else:
                cursor.execute(
                    """
                REPLACE INTO lesson(id, schedule_id, subject_name, teacher_name, startDate, endDate, startTime, endTime, repeat, dayOfWeek)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                    (
                        self.lesson_id,
                        self.schedule_id,
                        self.subject_name,
                        self.teacher_name,
                        self.startDate,
                        self.endDate,
                        self.startTime,
                        self.endTime,
                        self.repeat,
                        self.dayOfWeek,
                    ),
                )

            # Сохранение изменений
            conn.commit()
