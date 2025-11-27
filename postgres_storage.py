"""Модуль работы с PostgreSQL хранилищем паролей."""

import psycopg2
import hashlib
from typing import Dict, List


class PostgresPasswordStorage:
    """Класс для безопасного хранения паролей в PostgreSQL."""
    
    def __init__(self, connection_string: str, master_password: str):
        """Инициализирует PostgreSQL хранилище.
        
        Args:
            connection_string (str): Строка подключения к PostgreSQL.
            master_password (str): Мастер-пароль для доступа к хранилищу.
        """
        self.connection_string = connection_string
        self.master_hash = self._hash_password(master_password)
        self._init_database()
    
    def _get_connection(self):
        """Создает подключение к PostgreSQL."""
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Не удалось подключиться к PostgreSQL: {e}")
    
    def _init_database(self):
        """Инициализирует структуру базы данных."""
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                # Создаем ОДНУ таблицу для всего
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS passwords (
                        id SERIAL PRIMARY KEY,
                        service VARCHAR(255) UNIQUE NOT NULL,
                        username VARCHAR(255) NOT NULL,
                        password_hash VARCHAR(64) NOT NULL,
                        master_hash VARCHAR(64) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Проверяем мастер-пароль
                cur.execute("SELECT COUNT(*) FROM passwords WHERE master_hash = %s", (self.master_hash,))
                count = cur.fetchone()[0]
                
                if count == 0:
                    # Первый запуск - создаем тестовую запись для проверки мастер-пароля
                    cur.execute("""
                        INSERT INTO passwords (service, username, password_hash, master_hash) 
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (service) DO NOTHING
                    """, ("_master_check", "system", "dummy", self.master_hash))
                
                conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Хеширует пароль с использованием SHA-256.
        
        Args:
            password (str): Пароль для хеширования.
        
        Returns:
            str: Хеш пароля в шестнадцатеричном формате.
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def store_password(self, service: str, username: str, password: str):
        """Сохраняет пароль для указанного сервиса.
        
        Args:
            service (str): Название сервиса.
            username (str): Имя пользователя.
            password (str): Пароль для сохранения.
        
        Raises:
            ValueError: Если сервис уже существует.
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                # Проверяем существование сервиса
                cur.execute("SELECT id FROM passwords WHERE service = %s AND service != '_master_check'", (service,))
                if cur.fetchone():
                    raise ValueError(f"Сервис '{service}' уже существует")

                # Сохраняем пароль
                password_hash = self._hash_password(password)
                cur.execute(
                    "INSERT INTO passwords (service, username, password_hash, master_hash) VALUES (%s, %s, %s, %s)",
                    (service, username, password_hash, self.master_hash)
                )
                conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def verify_password(self, service: str, password: str) -> bool:
        """Проверяет правильность пароля для указанного сервиса.
        
        Args:
            service (str): Название сервиса.
            password (str): Пароль для проверки.
        
        Returns:
            bool: True если пароль верный, False в противном случае.
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                # Сначала проверяем мастер-пароль
                cur.execute("SELECT COUNT(*) FROM passwords WHERE master_hash = %s", (self.master_hash,))
                if cur.fetchone()[0] == 0:
                    return False
                
                # Проверяем пароль сервиса
                cur.execute(
                    "SELECT password_hash FROM passwords WHERE service = %s AND service != '_master_check'",
                    (service,)
                )
                result = cur.fetchone()
                if not result:
                    return False
                
                stored_hash = result[0]
                return stored_hash == self._hash_password(password)
        except Exception as e:
            return False
        finally:
            if conn:
                conn.close()
    
    def find_service(self, service_name: str) -> Dict[str, Dict]:
        """Находит сервисы по частичному совпадению названия.
        
        Args:
            service_name (str): Название сервиса или его часть для поиска.
        
        Returns:
            Dict[str, Dict]: Словарь найденных сервисов.
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT service, username FROM passwords WHERE service ILIKE %s AND service != '_master_check'",
                    (f'%{service_name}%',)
                )
                results = cur.fetchall()
                
                return {
                    service: {'username': username}
                    for service, username in results
                }
        except Exception as e:
            return {}
        finally:
            if conn:
                conn.close()
    
    def delete_password(self, service: str) -> bool:
        """Удаляет пароль для указанного сервиса.
        
        Args:
            service (str): Название сервиса.
        
        Returns:
            bool: True если пароль удален, False если не найден.
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM passwords WHERE service = %s AND service != '_master_check'", (service,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            return False
        finally:
            if conn:
                conn.close()
    
    def get_all_services(self) -> List[str]:
        """Возвращает список всех сервисов.
        
        Returns:
            List[str]: Список названий сервисов.
        """
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT service FROM passwords WHERE service != '_master_check' ORDER BY service")
                return [row[0] for row in cur.fetchall()]
        except Exception as e:
            return []
        finally:
            if conn:
                conn.close()