import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO


sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Добавляем путь для импорта

from commands import PasswordCommands
from storage import PasswordStorage


class TestPasswordCommands(unittest.TestCase): #Тесты для класса PasswordCommands
    
    
    def setUp(self): #Настройка перед каждым тестом
        self.commands = PasswordCommands() 
        test_files = ['test_passwords.json', 'passwords.json']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                
    def test_commands_inicialization(self): #Тест инициализации PasswordCommands
        print("Тест инициализации")
        self.assertIsNotNone(self.commands.generator)
        self.assertIsNotNone(self.commands.storage)
        print("PasswordCommands успешно инициализирован")
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_basic(self, mock_stdout):
        print("Тест базовой генерации пароля")
        
        #Создаем mock аргументы
        args = MagicMock()
        args.length = 12
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Пароль:", output)
        self.assertIn("Длина пароля: 12", output)
        self.assertIn("Сила пароля:", output)
        print("Базовая генерация пароля работает")
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_custom_len(self, mock_stdout):
        print("Тест генерации с кастомной длиной")
        
        args = MagicMock()
        args.length = 16
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Длина пароля: 16", output)
        print("Генерация с кастомной длиной работает")
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_no_special_chars(self, mock_stdout):
        print("Тест генерации без спецсимволов")
        
        args = MagicMock()
        args.length = 12
        args.uppercase = True
        args.digits = True
        args.special = False
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        print("Генерация без спецсимволов работает")
        
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_only_lowercase(self, mock_stdout):
        print("Тест генерации только строчных букв")
        
        args = MagicMock()
        args.length = 10
        args.uppercase = False
        args.digits = False
        args.special = False
        args.save = False
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        print("Генерация только строчных букв работает")
        
        
    @patch('builtins.input')
    @patch('getpass.getpass')
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_command_with_save(self, mock_stdout, mock_getpass, mock_input):
        print("Тест генерации с сохранением")
        
        mock_input.side_effect = ["Yandex", "Yandrex_testuser@yeandex.ru"] # Настраиваем mock для ввода пользователя
        mock_getpass.return_value = "qwerty123"
        
        args = MagicMock()
        args.length = 12
        args.uppercase = True
        args.digits = True
        args.special = True
        args.save = True
        
        self.commands.generate_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("Пароль:", output)
        self.assertIn("сохранен", output.lower())
        print("Генерация с сохранением работает")
        
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_existing_service(self, mock_stdout):
        print("Тест поиска существующего сервиса")
        
        # сохраняем тестовые данные
        self.commands.storage.store_password(
            "github", "Andrew09127", "GitHubPassQwerty", "master123"
        ) 
    
    
        args = MagicMock()
        args.service = "github"
    
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("github", output.lower())
        self.assertIn("Andrew09127", output)
        print("Поиск существующего сервиса работает")
        
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_partial_name(self, mock_stdout):
        print("Тест поиска по части имени")
        
        self.commands.storage.store_password("github", "Andrew09127", "GitHubPassQwerty", "master123") # Сохраняем несколько тестовых данных
        self.commands.storage.store_password("yandex", "padalkoandrej@yandex.ru", "YandexPass456", "master123")
        self.commands.storage.store_password("Kiinopoisk", "ANDREY_KINOPOISK", "QWERTY09127", "master123")
        
        args = MagicMock()
        args.service = "git"  # Частичное совпадение
        
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("git", output.lower())
        print("Поиск по части имени работает")
        
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_nonexistent_service(self, mock_stdout):
        print("Тест поиска несуществующего сервиса")
        
        args = MagicMock()
        args.service = "Okko123"
        
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("не найдены", output.lower() or "no services", output.lower())
        print("Поиск несуществующего сервиса работает")
        
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_command_case_insensitive(self, mock_stdout):
        print("Тест поиска без учета регистра")
        
        self.commands.storage.store_password("GitHub", "Andrew09127", "GitHubPassQwerty", "master123")
        
        args = MagicMock()
        args.service = "GITHUB"  # В верхнем регистре
        
        self.commands.find_command(args)
        
        output = mock_stdout.getvalue()
        self.assertIn("github", output.lower())
        print("Поиск без учета регистра работает")
        
    
def test_password_strength_display():
    print("Тест отображения сложности пароля")
    
    commands = PasswordCommands()
    
    # Создаем mock аргументы для генерации сильного пароля
    args = MagicMock()
    args.length = 16
    args.uppercase = True
    args.digits = True
    args.special = True
    args.save = False
    
    # Перехватываем вывод
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        commands.generate_command(args)
        output = mock_stdout.getvalue()
        
        # Проверяем, что отображается информация о сложности
        assert "Сила пароля:" in output
        assert "Длина пароля:" in output
        print("Отображение сложности пароля работает")
        
        
def test_multiple_operations():
    print("Тест нескольких операций подряд")
    
    commands = PasswordCommands()
    
    commands.storage =  PasswordStorage('test_multiple_operations.json')
    
    master_password = "testmaster123"
    
    # Сохраняем несколько паролей
    commands.storage.store_password("service_1", "user1", "pass1", master_password)
    commands.storage.store_password("service_2", "user2", "pass2", master_password)
    commands.storage.store_password("service_3", "user3", "pass3", master_password)
    
    # Ищем сервисы
    args = MagicMock()
    args.service = "service"
    
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        commands.find_command(args)
        output = mock_stdout.getvalue()
        
        # Должны найти все три сервиса
        assert "service_1" in output.lower()
        assert "service_2" in output.lower() 
        assert "service_3" in output.lower()
        print("Множественные операции работают")
        
    if os.path.exists('test_multiple_operations.json'):
        os.remove('test_multiple_operations.json')
        
#временно уберем интерактивную провеку
# def interactive_commands_test():
#     print("ИНТЕРАКТИВНЫЙ ТЕСТ COMMANDS.PY")
    
#     commands = PasswordCommands()
    
#     test_cases = [
#         {
#             'name': 'Короткий пароль',
#             'args': {'length':8, 'uppercase': True, 'digits': True, 'special': True, 'save': False}
#         },
#         {
#             'name': 'Длинный пароль',
#             'args': {'length': 20, 'uppercase': True, 'digits': True, 'special': True, 'save': False}
#         },
#         {
#             'name': 'Только буквы',
#             'args': {'length': 12, 'uppercase': True, 'digits': False, 'special': False, 'save': False}
#         },
#         {
#             'name': 'Только буквы и цифры',
#             'args': {'length': 10, 'uppercase': True, 'digits': True, 'special': False, 'save': False}
#         }
#     ]
    
#     for i, test_case in enumerate(test_cases, 1):
#         print(f"Тест {i}: {test_case['name']}")
        
#         args = MagicMock()
#         for key, value in test_case['args'].items():
#             setattr(args, key, value)
            
#         with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
#             commands.generate_command(args)
#             print(mock_stdout.getvalue())
            
            
#     print("Тест поиска сервисов")
    
#     # Сначала сохраним тестовые данные
#     commands.storage.store_password("github", "Andrew09127", "GitHubPassQwerty", "master123")
#     commands.storage.store_password("yandex", "padalkoandrej@yandex.ru", "YandexPass456", "master123")
    
#     args = MagicMock()
#     args.service = 'yan'
    
#     with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
#         commands.find_command(args)
#         print(mock_stdout.getvalue())
        
def run_all_commands_tests():
    print("ЗАПУСК ВСЕХ ТЕСТОВ COMMANDS.PY")
    
    # Запускаем unittest тесты
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPasswordCommands)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Запускаем дополнительные тесты
    test_password_strength_display()
    test_multiple_operations()
    
    print("ВСЕ ТЕСТЫ COMMANDS.PY ЗАВЕРШЕНЫ")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        #if sys.argv[1] == "interactive": 
            #interactive_commands_test()
        if sys.argv[1] == "unit":
            run_all_commands_tests()
        else:
            print("Использование:")
            print("python test_commands.py              # Все тесты")
            print("python test_commands.py interactive  # Интерактивный тест")
            print("python test_commands.py unit         # Только unit-тесты")
    else:
        # По умолчанию запускаем все
        run_all_commands_tests()
        #interactive_commands_test()    