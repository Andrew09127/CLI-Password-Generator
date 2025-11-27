"""Модуль тестирования для commands.py.

Содержит unit-тесты для класса PasswordCommands и его методов.
Тесты проверяют функциональность генерации паролей, поиска сервисов и управления хранилищем.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO


# Добавляем путь для импорта модулей проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commands import PasswordCommands
from storage import PasswordStorage


class TestPasswordCommands(unittest.TestCase):
    """Тестовый класс для проверки функциональности PasswordCommands.
    
    Attributes:
        commands (PasswordCommands): Экземпляр тестируемого класса.
    """
    
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом.
        
        Инициализирует экземпляр PasswordCommands и очищает тестовые файлы.
        """
        self.commands = PasswordCommands()
        self._cleanup_test_files()
    
    def tearDown(self):
        """Очистка тестового окружения после каждого теста.
        
        Удаляет созданные в процессе тестирования файлы.
        """
        self._cleanup_test_files()
    
    def _cleanup_test_files(self):
        """Удаляет тестовые файлы паролей."""
        test_files = ['test_passwords.json', 'passwords.json', 'test_multiple_operations.json']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_commands_initialization(self):
        """Тестирует корректность инициализации PasswordCommands.
        
        Проверяет, что генератор и хранилище инициализированы правильно.
        """
        self.assertIsNotNone(self.commands.generator, 
                           "Генератор паролей должен быть инициализирован")
        self.assertIsNotNone(self.commands.storage, 
                           "Хранилище паролей должно быть инициализировано")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_basic(self, mock_stdout):
        """Тестирует базовую генерацию пароля с параметрами по умолчанию.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        args = MagicMock()
        args.length = 12
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Пароль:", output, 
                     "В выводе должна отображаться сгенерированный пароль")
        self.assertIn("Длина пароля: 12", output, 
                     "В выводе должна отображаться длина пароля")
        self.assertIn("Сила пароля:", output, 
                     "В выводе должна отображаться оценка сложности пароля")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_custom_length(self, mock_stdout):
        """Тестирует генерацию пароля с пользовательской длиной.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        args = MagicMock()
        args.length = 16
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Длина пароля: 16", output, 
                     "В выводе должна отображаться указанная длина пароля")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_no_special_chars(self, mock_stdout):
        """Тестирует генерацию пароля без специальных символов.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        args = MagicMock()
        args.length = 12
        args.uppercase = True
        args.digits = True
        args.special = False
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Пароль:", output, 
                     "Пароль должен быть сгенерирован без специальных символов")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_only_lowercase(self, mock_stdout):
        """Тестирует генерацию пароля только из строчных букв.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        args = MagicMock()
        args.length = 10
        args.uppercase = False
        args.digits = False
        args.special = False
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Пароль:", output, 
                     "Пароль должен быть сгенерирован только из строчных букв")
    
    @patch('builtins.input')
    @patch('getpass.getpass')
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_with_save(self, mock_stdout, mock_getpass, mock_input):
        """Тестирует генерацию пароля с последующим сохранением.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
            mock_getpass: Mock объект для имитации ввода мастер-пароля.
            mock_input: Mock объект для имитации ввода названия сервиса.
        """
        mock_input.side_effect = ["Yandex", "testuser@yandex.ru"]
        mock_getpass.return_value = "qwerty123"
        
        args = MagicMock()
        args.length = 12
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = True
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Пароль:", output, 
                     "Должен отображаться сгенерированный пароль")
        self.assertIn("сохранен", output.lower(), 
                     "Должно подтверждаться сохранение пароля")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_existing_service(self, mock_stdout):
        """Тестирует поиск существующего сервиса.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        # Сохраняем тестовые данные
        self.commands.storage.store_password(
            "github", "Andrew09127", "GitHubPassQwerty", "master123"
        )
        
        args = MagicMock()
        args.service = "github"
        
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("github", output.lower(), 
                     "Должен находиться существующий сервис")
        self.assertIn("Andrew09127", output, 
                     "Должны отображаться данные пользователя")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_partial_name(self, mock_stdout):
        """Тестирует поиск сервисов по частичному совпадению названия.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        self.commands.storage.store_password("github", "Andrew09127", "GitHubPassQwerty", "master123")
        self.commands.storage.store_password("yandex", "test@yandex.ru", "YandexPass456", "master123")
        
        args = MagicMock()
        args.service = "git"  # Частичное совпадение
        
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("git", output.lower(), 
                     "Должны находиться сервисы по частичному совпадению")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_nonexistent_service(self, mock_stdout):
        """Тестирует поиск несуществующего сервиса.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        args = MagicMock()
        args.service = "Okko123"
        
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertTrue(
            "не найдены" in output.lower() or "no services" in output.lower(),
            "Должно сообщаться об отсутствии сервисов"
        )
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_case_insensitive(self, mock_stdout):
        """Тестирует поиск сервисов без учета регистра.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        self.commands.storage.store_password("GitHub", "Andrew09127", "GitHubPassQwerty", "master123")
        
        args = MagicMock()
        args.service = "GITHUB"  # В верхнем регистре
        
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("github", output.lower(), 
                     "Поиск должен работать без учета регистра")
    
    def test_password_strength_display(self):
        """Тестирует отображение информации о сложности пароля."""
        args = MagicMock()
        args.length = 16
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.commands.generate_command(args)
            output = mock_stdout.getvalue()
            
            self.assertIn("Сила пароля:", output, "Должна отображаться оценка сложности")
            self.assertIn("Длина пароля:", output, "Должна отображаться длина пароля")
    
    def test_multiple_operations(self):
        """Тестирует выполнение нескольких операций подряд."""
        self.commands.storage = PasswordStorage('test_multiple_operations.json')
        master_password = "testmaster123"
        
        # Сохраняем несколько паролей
        self.commands.storage.store_password("service_1", "user1", "pass1", master_password)
        self.commands.storage.store_password("service_2", "user2", "pass2", master_password)
        self.commands.storage.store_password("service_3", "user3", "pass3", master_password)
        
        # Ищем сервисы
        args = MagicMock()
        args.service = "service"
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.commands.find_command(args)
            output = mock_stdout.getvalue()
            
            self.assertIn("service_1", output.lower(), "Должен находиться service_1")
            self.assertIn("service_2", output.lower(), "Должен находиться service_2")
            self.assertIn("service_3", output.lower(), "Должен находиться service_3")
    
    def test_generate_min_length(self):
        """Тестирует генерацию пароля минимальной длины."""
        args = MagicMock()
        args.length = 8
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.commands.generate_command(args)
            output = mock_stdout.getvalue()
            
            self.assertIn("Длина пароля: 8", output, 
                         "В выводе должна отображаться минимальная длина пароля")
    
    def test_generate_max_length(self):
        """Тестирует генерацию пароля максимальной длины."""
        args = MagicMock()
        args.length = 50
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.commands.generate_command(args)
            output = mock_stdout.getvalue()
            
            self.assertIn("Длина пароля: 50", output, 
                         "В выводе должна отображаться максимальная длина пароля")


if __name__ == "__main__":
    unittest.main()