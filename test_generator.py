"""Модуль тестирования для generator.py.

Содержит unit-тесты для класса PasswordGenerator и его методов.
Тесты проверяют функциональность генерации паролей с различными параметрами.
"""

import unittest
from generator import PasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    """Тестовый класс для проверки функциональности PasswordGenerator.
    
    Attributes:
        generator (PasswordGenerator): Экземпляр тестируемого класса.
    """
    
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом.
        
        Инициализирует экземпляр PasswordGenerator.
        """
        self.generator = PasswordGenerator()
    
    def test_generate_default_parameters(self):
        """Тестирует генерацию пароля с параметрами по умолчанию.
        
        Проверяет, что пароль имеет правильную длину и содержит различные типы символов.
        """
        password = self.generator.generate()
        
        self.assertEqual(len(password), 12,
                        "Пароль по умолчанию должен иметь длину 12 символов")
        self.assertTrue(any(c.islower() for c in password),
                       "Пароль должен содержать строчные буквы")
        self.assertTrue(any(c.isupper() for c in password),
                       "Пароль должен содержать заглавные буквы")
        self.assertTrue(any(c.isdigit() for c in password),
                       "Пароль должен содержать цифры")
        self.assertTrue(any(not c.isalnum() for c in password),
                       "Пароль должен содержать специальные символы")
    
    def test_generate_custom_length(self):
        """Тестирует генерацию пароля с пользовательской длиной.
        
        Проверяет корректность работы с различными длинами паролей.
        """
        test_lengths = [8, 15, 20]
        
        for length in test_lengths:
            with self.subTest(length=length):
                password = self.generator.generate(length=length)
                self.assertEqual(len(password), length,
                               f"Пароль должен иметь длину {length} символов")
    
    def test_generate_without_uppercase(self):
        """Тестирует генерацию пароля без заглавных букв.
        
        Проверяет, что пароль не содержит заглавных букв при отключенной опции.
        """
        password = self.generator.generate(use_uppercase=False)
        
        self.assertFalse(any(c.isupper() for c in password),
                        "Пароль не должен содержать заглавные буквы")
        self.assertTrue(any(c.islower() for c in password),
                       "Пароль должен содержать строчные буквы")
    
    def test_generate_without_digits(self):
        """Тестирует генерацию пароля без цифр.
        
        Проверяет, что пароль не содержит цифр при отключенной опции.
        """
        password = self.generator.generate(use_digits=False)
        
        self.assertFalse(any(c.isdigit() for c in password),
                        "Пароль не должен содержать цифры")
    
    def test_generate_without_special_chars(self):
        """Тестирует генерацию пароля без специальных символов.
        
        Проверяет, что пароль не содержит специальных символов при отключенной опции.
        """
        password = self.generator.generate(use_special=False)
        
        self.assertFalse(any(not c.isalnum() for c in password),
                        "Пароль не должен содержать специальные символы")
        self.assertTrue(all(c.isalnum() for c in password),
                       "Все символы пароля должны быть буквенно-цифровыми")
    
    def test_generate_only_lowercase(self):
        """Тестирует генерацию пароля только из строчных букв.
        
        Проверяет минимальную конфигурацию пароля.
        """
        password = self.generator.generate(use_uppercase=False, 
                                         use_digits=False, 
                                         use_special=False)
        
        self.assertTrue(all(c.islower() for c in password),
                       "Пароль должен содержать только строчные буквы")
        self.assertFalse(any(c.isupper() for c in password),
                        "Пароль не должен содержать заглавные буквы")
        self.assertFalse(any(c.isdigit() for c in password),
                        "Пароль не должен содержать цифры")
        self.assertFalse(any(not c.isalnum() for c in password),
                        "Пароль не должен содержать специальные символы")
    
    def test_generate_contains_required_char_types(self):
        """Тестирует гарантированное наличие выбранных типов символов в пароле.
        
        Проверяет, что пароль содержит хотя бы один символ каждого включенного типа.
        """
        # Тест с включенными всеми типами символов
        password = self.generator.generate(use_uppercase=True, 
                                         use_digits=True, 
                                         use_special=True)
        
        self.assertTrue(any(c.isupper() for c in password),
                       "Пароль должен содержать хотя бы одну заглавную букву")
        self.assertTrue(any(c.isdigit() for c in password),
                       "Пароль должен содержать хотя бы одну цифру")
        self.assertTrue(any(not c.isalnum() for c in password),
                       "Пароль должен содержать хотя бы один специальный символ")
    
    def test_password_uniqueness(self):
        """Тестирует уникальность генерируемых паролей.
        
        Проверяет, что последовательно сгенерированные пароли различаются.
        """
        passwords = set()
        
        for _ in range(10):
            password = self.generator.generate()
            passwords.add(password)
        
        self.assertEqual(len(passwords), 10,
                        "Все сгенерированные пароли должны быть уникальными")
    
    def test_chars_sets_initialization(self):
        """Тестирует корректность инициализации наборов символов.
        
        Проверяет, что все необходимые наборы символов присутствуют.
        """
        expected_sets = ['lowercase', 'uppercase', 'digits', 'special']
        
        for char_set in expected_sets:
            with self.subTest(char_set=char_set):
                self.assertIn(char_set, self.generator.chars_sets,
                             f"Набор символов '{char_set}' должен быть определен")
                self.assertIsInstance(self.generator.chars_sets[char_set], str,
                                    f"Набор символов '{char_set}' должен быть строкой")
                self.assertGreater(len(self.generator.chars_sets[char_set]), 0,
                                 f"Набор символов '{char_set}' не должен быть пустым")


def run_comprehensive_generator_test():
    """Запускает комплексное тестирование генератора паролей.
    
    Выполняет дополнительные проверки, не входящие в стандартные unit-тесты.
    """
    print("КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ГЕНЕРАТОРА ПАРОЛЕЙ")
    
    generator = PasswordGenerator()
    
    test_cases = [
        {
            'name': 'Пароль по умолчанию',
            'params': {'length': 12, 'use_uppercase': True, 'use_digits': True, 'use_special': True}
        },
        {
            'name': 'Короткий пароль',
            'params': {'length': 8, 'use_uppercase': True, 'use_digits': True, 'use_special': True}
        },
        {
            'name': 'Длинный сложный пароль',
            'params': {'length': 20, 'use_uppercase': True, 'use_digits': True, 'use_special': True}
        },
        {
            'name': 'Только строчные буквы',
            'params': {'length': 10, 'use_uppercase': False, 'use_digits': False, 'use_special': False}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}:")
        password = generator.generate(**test_case['params'])
        
        print(f"   Пароль: {password}")
        print(f"   Длина: {len(password)}")
        print(f"   Заглавные: {any(c.isupper() for c in password)}")
        print(f"   Цифры: {any(c.isdigit() for c in password)}")
        print(f"   Спецсимволы: {any(not c.isalnum() for c in password)}")
    
    print("\nТЕСТИРОВАНИЕ ЗАВЕРШЕНО")


def run_all_generator_tests():
    """Запускает все тесты для модуля generator.
    
    Выполняет как unittest тесты, так и дополнительные функциональные тесты.
    """
    print("ЗАПУСК ВСЕХ ТЕСТОВ GENERATOR.PY")
    
    # Запускаем unittest тесты
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPasswordGenerator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Запускаем дополнительные тесты
    run_comprehensive_generator_test()
    
    print("ВСЕ ТЕСТЫ GENERATOR.PY ЗАВЕРШЕНЫ")


if __name__ == "__main__":
    """Точка входа для запуска тестов.
    
    Поддерживает различные режимы запуска через аргументы командной строки.
    """
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "unit":
            # Запуск только unit-тестов
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromTestCase(TestPasswordGenerator)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        elif sys.argv[1] == "comprehensive":
            # Запуск только комплексного тестирования
            run_comprehensive_generator_test()
        else:
            print("Использование:")
            print("python test_generator.py              # Все тесты")
            print("python test_generator.py unit         # Только unit-тесты")
            print("python test_generator.py comprehensive # Только комплексное тестирование")
    else:
        # По умолчанию запускаем все тесты
        run_all_generator_tests()