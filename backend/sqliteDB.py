import sqlite3

# Подключение к БД (убедитесь, что путь верный)
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# Проверка списка таблиц
cursor.execute(
    """
 CREATE TABLE lesson (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER,
    teacher_name TEXT,
    subject_name TEXT,
    startDate DATE,
    endDate DATE,
    startTime TIME,
    endTime TIME,
    repeat INTEGER,
    dayOfWeek INTEGER,
    FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id));

"""
)

conn.close()
