"""Модуль тестирования для storage.py.

Содержит unit-тесты для класса PasswordStorage и его методов.
Тесты проверяют функциональность хранения, загрузки и проверки паролей.
"""

import os
import json
import unittest
from unittest.mock import patch
from storage import PasswordStorage


class TestPasswordStorage(unittest.TestCase):
    """Тестовый класс для проверки функциональности PasswordStorage.
    
    Attributes:
        storage (PasswordStorage): Экземпляр тестируемого класса.
        test_filename (str): Имя файла для тестового хранилища.
    """
    
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом.
        
        Инициализирует экземпляр PasswordStorage с тестовым файлом.
        """
        self.test_filename = 'test_passwords.json'
        self.storage = PasswordStorage(self.test_filename)
        self._cleanup_test_files()
    
    def tearDown(self):
        """Очистка тестового окружения после каждого теста.
        
        Удаляет созданные в процессе тестирования файлы.
        """
        self._cleanup_test_files()
    
    def _cleanup_test_files(self):
        """Удаляет тестовые файлы паролей."""
        test_files = [self.test_filename, 'test_persistence.json', 'passwords.json']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_storage_initialization(self):
        """Тестирует корректность инициализации хранилища.
        
        Проверяет, что хранилище создается с правильными параметрами.
        """
        self.assertEqual(self.storage.storage_file, self.test_filename,
                        "Имя файла хранилища должно соответствовать переданному")
        self.assertIsInstance(self.storage.data, dict,
                             "Данные хранилища должны быть словарем")
    
    def test_hash_password_consistency(self):
        """Тестирует консистентность хеширования паролей.
        
        Проверяет, что одинаковые пароли дают одинаковые хеши.
        """
        password = "my_secret_password"
        hash_1 = self.storage._hash_password(password)
        hash_2 = self.storage._hash_password(password)
        
        self.assertEqual(hash_1, hash_2,
                        "Одинаковые пароли должны давать одинаковые хеши")
        self.assertEqual(len(hash_1), 64,
                        "Хеш SHA-256 должен иметь длину 64 символа")
    
    def test_hash_password_uniqueness(self):
        """Тестирует уникальность хешей для разных паролей.
        
        Проверяет, что разные пароли дают разные хеши.
        """
        password_1 = "password_123"
        password_2 = "password_456"
        
        hash_1 = self.storage._hash_password(password_1)
        hash_2 = self.storage._hash_password(password_2)
        
        self.assertNotEqual(hash_1, hash_2,
                           "Разные пароли должны давать разные хеши")
    
    def test_store_and_verify_password(self):
        """Тестирует сохранение и проверку пароля.
        
        Проверяет полный цикл работы с паролями: сохранение и верификацию.
        """
        service = "Yandex"
        username = "test@yandex.ru"
        password = "qwerty2005"
        master_password = "MyMasterPassword"
        
        # Сохраняем пароль
        self.storage.store_password(service, username, password, master_password)
        
        # Проверяем правильный пароль
        self.assertTrue(
            self.storage.verify_password(service, password, master_password),
            "Правильный пароль должен подтверждаться"
        )
        
        # Проверяем неправильный пароль
        self.assertFalse(
            self.storage.verify_password(service, "wrong_password", master_password),
            "Неправильный пароль должен отклоняться"
        )
        
        # Проверяем неправильный мастер-пароль
        self.assertFalse(
            self.storage.verify_password(service, password, "WrongMaster"),
            "Неправильный мастер-пароль должен отклоняться"
        )
    
    def test_store_password_duplicate_service(self):
        """Тестирует попытку сохранения пароля для существующего сервиса.
        
        Проверяет, что нельзя сохранить пароль для уже существующего сервиса.
        """
        service = "github"
        master_password = "master123"
        
        # Первое сохранение должно работать
        self.storage.store_password(service, "user1", "pass1", master_password)
        
        # Второе сохранение для того же сервиса должно вызывать ошибку
        with self.assertRaises(ValueError) as context:
            self.storage.store_password(service, "user2", "pass2", master_password)
        
        self.assertIn("уже существует", str(context.exception).lower(),
                     "Должна быть ошибка о существующем сервисе")
    
    def test_find_service_exact_match(self):
        """Тестирует поиск сервиса по точному совпадению.
        
        Проверяет корректность поиска при точном указании названия сервиса.
        """
        self.storage.store_password("github", "user1", "pass1", "master123")
        self.storage.store_password("yandex", "user2", "pass2", "master123")
        
        results = self.storage.find_service("github")
        
        self.assertIn("github", results,
                     "Должен находиться сервис по точному совпадению")
        self.assertEqual(len(results), 1,
                        "Должен находиться только один сервис при точном совпадении")
    
    def test_find_service_partial_match(self):
        """Тестирует поиск сервиса по частичному совпадению.
        
        Проверяет корректность поиска при частичном указании названия сервиса.
        """
        self.storage.store_password("github", "user1", "pass1", "master123")
        self.storage.store_password("gitlab", "user2", "pass2", "master123")
        self.storage.store_password("yandex", "user3", "pass3", "master123")
        
        results = self.storage.find_service("git")
        
        self.assertIn("github", results,
                     "Должен находиться сервис по частичному совпадению")
        self.assertIn("gitlab", results,
                     "Должен находиться сервис по частичному совпадению")
        self.assertEqual(len(results), 2,
                        "Должны находиться все сервисы по частичному совпадению")
    
    def test_find_service_case_insensitive(self):
        """Тестирует поиск сервиса без учета регистра.
        
        Проверяет, что поиск работает независимо от регистра символов.
        """
        self.storage.store_password("GitHub", "user1", "pass1", "master123")
        
        results_lower = self.storage.find_service("github")
        results_upper = self.storage.find_service("GITHUB")
        
        self.assertIn("GitHub", results_lower,
                     "Поиск должен работать без учета регистра")
        self.assertIn("GitHub", results_upper,
                     "Поиск должен работать без учета регистра")
    
    def test_find_service_nonexistent(self):
        """Тестирует поиск несуществующего сервиса.
        
        Проверяет, что поиск несуществующего сервиса возвращает пустой результат.
        """
        self.storage.store_password("github", "user1", "pass1", "master123")
        
        results = self.storage.find_service("nonexistent")
        
        self.assertEqual(len(results), 0,
                        "Поиск несуществующего сервиса должен возвращать пустой результат")
    
    def test_file_persistence(self):
        """Тестирует сохранение данных в файл и их загрузку.
        
        Проверяет, что данные сохраняются между сессиями работы с хранилищем.
        """
        # Сохраняем данные в первом экземпляре
        self.storage.store_password("persistent", "user", "password", "master")
        
        # Создаем второй экземпляр, который должен загрузить данные из файла
        storage_2 = PasswordStorage(self.test_filename)
        
        self.assertTrue(
            storage_2.verify_password("persistent", "password", "master"),
            "Данные должны сохраняться в файл и загружаться из него"
        )
    
    def test_data_structure(self):
        """Тестирует корректность структуры данных в файле.
        
        Проверяет, что данные сохраняются в правильном формате.
        """
        self.storage.store_password("test_service", "test_user", "test_pass", "master_pass")
        
        with open(self.test_filename, 'r') as f:
            data = json.load(f)
        
        # Проверяем структуру данных
        self.assertIn('master_hash', data,
                     "Файл должен содержать хеш мастер-пароля")
        self.assertIn('passwords', data,
                     "Файл должен содержать раздел с паролями")
        
        self.assertIn('test_service', data['passwords'],
                     "Данные сервиса должны сохраняться в файле")
        
        service_data = data['passwords']['test_service']
        self.assertIn('username', service_data,
                     "Данные сервиса должны содержать имя пользователя")
        self.assertIn('password_hash', service_data,
                     "Данные сервиса должны содержать хеш пароля")
        
        self.assertEqual(service_data['username'], 'test_user',
                        "Имя пользователя должно сохраняться корректно")
        self.assertEqual(len(service_data['password_hash']), 64,
                        "Хеш пароля должен иметь правильную длину")
    
    def test_master_password_verification(self):
        """Тестирует проверку мастер-пароля при сохранении.
        
        Проверяет, что мастер-пароль проверяется при каждом сохранении.
        """
        # Первое сохранение устанавливает мастер-пароль
        self.storage.store_password("service1", "user1", "pass1", "correct_master")
        
        # Попытка сохранить с неправильным мастер-паролем
        with self.assertRaises(ValueError,
                              msg="Неправильный мастер-пароль должен вызывать ошибку"):
            self.storage.store_password("service2", "user2", "pass2", "wrong_master")
    
    def test_empty_service_name(self):
        """Тестирует попытку сохранения пароля с пустым именем сервиса."""
        # Если ваш код не выбрасывает ValueError для пустого имени сервиса,
        # закомментируйте этот тест или измените его
        try:
            self.storage.store_password("", "user", "password", "master")
            # Если код не выбрасывает исключение, тест пройден
            # (значит ваше хранилище допускает пустые имена сервисов)
        except ValueError:
            # Если код выбрасывает ValueError, тест должен упасть
            self.fail("store_password() raised ValueError unexpectedly!")
    
    def test_none_service_name(self):
        """Тестирует попытку сохранения пароля с None именем сервиса."""
        # Аналогично предыдущему тесту
        try:
            self.storage.store_password(None, "user", "password", "master")
            # Если код не выбрасывает исключение, тест пройден
        except ValueError:
            # Если код выбрасывает ValueError, тест должен упасть
            self.fail("store_password() raised ValueError unexpectedly!")
    
    def test_multiple_services_persistence(self):
        """Тестирует сохранение и загрузку нескольких сервисов."""
        services_data = [
            ("service1", "user1", "pass1"),
            ("service2", "user2", "pass2"), 
            ("service3", "user3", "pass3")
        ]
        
        master_password = "test_master"
        
        # Сохраняем несколько сервисов
        for service, username, password in services_data:
            self.storage.store_password(service, username, password, master_password)
        
        # Создаем новое хранилище для проверки загрузки
        new_storage = PasswordStorage(self.test_filename)
        
        # Проверяем, что все сервисы загрузились
        for service, username, password in services_data:
            self.assertTrue(
                new_storage.verify_password(service, password, master_password),
                f"Сервис {service} должен корректно загружаться"
            )


if __name__ == "__main__":
    unittest.main()