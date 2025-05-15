import sqlite3

# Подключение к базе данных (файл создастся автоматически)
with sqlite3.connect("my_database.db") as conn:
    # Создание курсора
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute(
        """
    DELETE FROM lesson

    """
    )


# Сохранение изменений
conn.commit()

# Закрытие соединения
conn.close()
