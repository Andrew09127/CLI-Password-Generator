"""
Простая реализация хранилища паролей на PostgreSQL с использованием psycopg2.

Модуль предоставляет класс PostgresStorage для работы с базой данных PostgreSQL,
который заменяет CSV-операции
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from contextlib import contextmanager
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Загружаем переменные окружения из файла .env
load_dotenv(encoding='utf-8')

# Параметры подключения к PostgreSQL
PG_HOST = os.environ.get("PG_HOST", "localhost")
PG_PORT = os.environ.get("PG_PORT", "5433")
PG_DB = os.environ.get("PG_DB", "PasswordDB")
PG_USER = os.environ.get("PG_USER", "PasswordDB")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "mypassword123")

print(f"DEBUG - Подключение: {PG_USER}@{PG_HOST}:{PG_PORT}/{PG_DB}")


def get_conn() -> psycopg2.extensions.connection:
    """
    Создает и возвращает соединение с базой данных PostgreSQL.
    
    Returns:
        psycopg2.extensions.connection: Объект соединения с базой данных
        
    Raises:
        psycopg2.OperationalError: Если не удалось подключиться к базе данных
    """
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )


@contextmanager
def conn_cursor():
    """
    Контекстный менеджер для работы с соединением и курсором.
    
    Обеспечивает:
    - Автоматическое создание и закрытие соединения
    - Автоматический коммит при успешном выполнении
    - Откат изменений при возникновении исключения
    - Использование RealDictCursor для возврата результатов в виде словарей
    
    Yields:
        tuple: Кортеж (connection, cursor) для работы с базой данных
    """
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """
    Создает таблицу 'passwords' в базе данных, если она не существует.
    
    Таблица содержит следующие поля:
    - id: SERIAL PRIMARY KEY - уникальный идентификатор записи
    - name: TEXT - название/описание пароля
    - password: TEXT NOT NULL - сам пароль
    - length: INTEGER - длина пароля
    - charset: TEXT - набор символов, использованный для генерации
    - created_at: TIMESTAMP WITH TIME ZONE - дата и время создания (автоматически)
    - meta: JSONB - дополнительные метаданные в формате JSON
    
    Raises:
        psycopg2.Error: Если произошла ошибка при создании таблицы
    """
    create_query = """
    CREATE TABLE IF NOT EXISTS passwords (
        id SERIAL PRIMARY KEY,
        name TEXT,
        password TEXT NOT NULL,
        length INTEGER,
        charset TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
        meta JSONB
    );
    """
    try:
        with conn_cursor() as (conn, cur):
            cur.execute(create_query)
        print("Таблица 'passwords' создана успешно!")
    except Exception as e:
        print(f"Ошибка создания таблицы: {e}")
        raise


class PostgresStorage:
    """Класс для работы с хранилищем паролей в PostgreSQL."""
    
    def __init__(self) -> None:
        """
        Инициализирует хранилище.
        
        При создании экземпляра автоматически создает таблицу 'passwords',
        если она еще не существует в базе данных.
        """
        init_db()
    
    def save_entry(self, entry: Dict[str, Any]) -> int:
        """
        Сохраняет запись о пароле в базу данных.
        
        Args:
            entry: Словарь с данными пароля. Должен содержать:
                - password (обязательно): строка с паролем
                - name (опционально): название/описание
                - length (опционально): длина пароля
                - charset (опционально): набор символов
                - meta (опционально): дополнительные метаданные в виде словаря
                
        Returns:
            int: ID сохраненной записи
            
        Raises:
            KeyError: Если отсутствует обязательное поле 'password'
            psycopg2.Error: Если произошла ошибка при сохранении в БД
        """
        query = """
        INSERT INTO passwords (name, password, length, charset, meta)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        # Подготавливаем метаданные для сохранения в JSONB
        meta = entry.get("meta")
        if meta is not None and not isinstance(meta, (str, bytes)):
            meta = Json(meta)
        
        with conn_cursor() as (conn, cur):
            cur.execute(query, (
                entry.get("name"),
                entry["password"],
                entry.get("length"),
                entry.get("charset"),
                meta
            ))
            row = cur.fetchone()
            return row["id"]
    
    def get_all(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Возвращает все записи из базы данных.
        
        Args:
            limit: Максимальное количество возвращаемых записей (по умолчанию 1000)
            
        Returns:
            List[Dict[str, Any]]: Список словарей с записями, отсортированный
            по дате создания в порядке убывания (новые записи первыми)
        """
        query = "SELECT * FROM passwords ORDER BY created_at DESC LIMIT %s;"
        with conn_cursor() as (conn, cur):
            cur.execute(query, (limit,))
            return cur.fetchall()
    
    def get_by_id(self, id_: int) -> Optional[Dict[str, Any]]:
        """
        Возвращает запись по её ID.
        
        Args:
            id_: Целочисленный идентификатор записи
            
        Returns:
            Optional[Dict[str, Any]]: Словарь с данными записи или None,
            если запись с указанным ID не найдена
        """
        query = "SELECT * FROM passwords WHERE id = %s;"
        with conn_cursor() as (conn, cur):
            cur.execute(query, (id_,))
            return cur.fetchone()
    
    def delete(self, id_: int) -> int:
        """
        Удаляет запись по её ID.
        
        Args:
            id_: Целочисленный идентификатор записи для удаления
            
        Returns:
            int: Количество удаленных записей (0 или 1)
        """
        query = "DELETE FROM passwords WHERE id = %s;"
        with conn_cursor() as (conn, cur):
            cur.execute(query, (id_,))
            return cur.rowcount
    
    def close(self) -> None:
        """
        Закрывает ресурсы хранилища.
        
        В текущей реализации метод является заглушкой для совместимости
        с другими хранилищами. Реальное соединение закрывается автоматически
        после каждого запроса.
        """
        pass


def get_storage() -> PostgresStorage:
    """
    Фабричная функция для создания экземпляра PostgresStorage.
    
    Returns:
        PostgresStorage: Новый экземпляр класса хранилища
    """
    return PostgresStorage()


if __name__ == "__main__":
    # Пример использования хранилища
    storage = PostgresStorage()
    
    # Сохранение тестовой записи
    test_entry = {
        "name": "Тестовый пароль",
        "password": "test_password_123",
        "length": 16,
        "charset": "letters+digits+symbols",
        "meta": {"category": "test", "strength": "high"}
    }
    
    try:
        entry_id = storage.save_entry(test_entry)
        print(f"Сохранена запись с ID: {entry_id}")
        
        # Получение всех записей
        all_entries = storage.get_all()
        print(f"Всего записей в базе: {len(all_entries)}")
        
        # Получение конкретной записи
        entry = storage.get_by_id(entry_id)
        if entry:
            print(f"Получена запись: {entry['name']} - {entry['password']}")
            
        # Удаление записи
        deleted = storage.delete(entry_id)
        print(f"Удалено записей: {deleted}")
        
    except Exception as e:
        print(f"Ошибка при работе с хранилищем: {e}")