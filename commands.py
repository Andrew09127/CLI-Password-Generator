"""Модуль команд CLI для управления паролями.

Содержит класс PasswordCommands, который реализует команды для:
- генерации паролей
- управления базой данных паролей
- поиска и проверки сохраненных паролей
"""

from generator import PasswordGenerator
from postgres_storage import PostgresStorage
from utils import print_password_information
from getpass import getpass


class PasswordCommands:
    """Класс, реализующий команды CLI для работы с паролями."""
    
    def __init__(self):
        """Инициализирует генератор паролей и хранилище данных."""
        self.generator = PasswordGenerator()
        self.storage = PostgresStorage()

    def init_db(self) -> None:
        """Инициализирует базу данных.
        
        Создает таблицу для хранения паролей, если она не существует.
        
        Raises:
            Exception: Если произошла ошибка при создании таблицы.
        """
        try:
            from postgres_storage import init_db
            init_db()
            print("База данных успешно инициализирована!")
            print("Таблица 'passwords' создана.")
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")
    
    def generate_command(self, args) -> None:
        """Генерирует пароль с заданными параметрами.
        
        Args:
            args: Объект аргументов командной строки, содержащий:
                - length: Длина генерируемого пароля
                - uppercase: Флаг использования заглавных букв
                - digits: Флаг использования цифр
                - special: Флаг использования специальных символов
                - save: Флаг сохранения пароля в базу данных
        
        Опционально сохраняет пароль в базу данных, если установлен флаг --save.
        При сохранении запрашивает у пользователя дополнительную информацию.
        
        Raises:
            Exception: Если произошла ошибка при сохранении в базу данных.
        """
        password = self.generator.generate(
            length=args.length,
            use_uppercase=args.uppercase,
            use_digits=args.digits,
            use_special=args.special
        )

        print_password_information(password)

        if args.save:
            service = input("Введите название сервиса: ")
            username = input("Введите имя пользователя: ")
            master_password = getpass("Введите мастер-пароль: ")

            try:
                entry = {
                    "name": service,
                    "password": password,
                    "length": args.length,
                    "charset": "auto",
                    "meta": {"username": username}
                }

                new_id = self.storage.save_entry(entry)
                print(f"Пароль сохранён в БД (id={new_id})!")

            except Exception as e:
                print(f"Ошибка сохранения: {e}")

    def find_command(self, args) -> None:
        """Ищет сервисы в базе данных по названию.
        
        Args:
            args: Объект аргументов командной строки, содержащий:
                - service: Строка для поиска в названиях сервисов
        
        Поиск осуществляется без учета регистра. Выводит список найденных сервисов
        с их идентификаторами и именами пользователей.
        
        Raises:
            Exception: Если произошла ошибка при обращении к базе данных.
        """
        service_name = args.service.lower()

        try:
            rows = self.storage.get_all()

            results = [
                r for r in rows
                if service_name in r["name"].lower()
            ]

            if results:
                print(f"Найдено {len(results)} сервисов:")
                for r in results:
                    print(f" {r['id']}: {r['name']} (user={r['meta'].get('username')})")
            else:
                print("Сервисы не найдены")

        except Exception as e:
            print(f"Ошибка поиска: {e}")

    def verify_command(self, args) -> None:
        """Проверяет правильность пароля для указанного сервиса.
        
        Args:
            args: Объект аргументов командной строки, содержащий:
                - service: Название сервиса для проверки пароля
        
        Запрашивает у пользователя пароль и мастер-пароль (последний в текущей
        реализации не используется, но оставлен для будущей функциональности).
        Сравнивает введенный пароль с сохраненным в базе данных.
        
        Raises:
            Exception: Если произошла ошибка при обращении к базе данных.
        """
        service = args.service

        try:
            rows = self.storage.get_all()
            entry = next((r for r in rows if r["name"] == service), None)

            if not entry:
                print("Сервис не найден")
                return

            password = getpass("Введите пароль для проверки: ")
            master_password = getpass("Введите мастер-пароль: ")

            if password == entry["password"]:
                print("Пароль верный!")
            else:
                print("Пароль неверный!")

        except Exception as e:
            print(f"Ошибка проверки: {e}")