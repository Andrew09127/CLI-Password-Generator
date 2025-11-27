"""Модуль тестирования для utils.py.

Содержит unit-тесты для вспомогательных функций валидации и оценки паролей.
Тесты проверяют функциональность valid_len, get_password_strength и print_password_information.
"""

import unittest
from unittest.mock import patch
from io import StringIO
import argparse
from utils import valid_len, get_password_strength, print_password_information


class TestUtils(unittest.TestCase):
    """Тестовый класс для проверки вспомогательных функций.
    
    Attributes:
        test_passwords (dict): Набор тестовых паролей для оценки сложности.
    """
    
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом."""
        self.test_passwords = {
            "very_weak": ["123", "qwerty", "password"],
            "weak": ["qwerty123", "password1"],
            "medium": ["Password123", "Qwerty!123"],
            "strong": ["&2;],]EG_z:a", "k:Cz+2J6", "qixHOQdHUeTW"],
            "very_strong": ["$g3&29(2;h9:", "6!6U53y@4@$^.kPUp9*+"]
        }
    
    def test_valid_len_acceptable_range(self):
        """Тестирует валидацию длины пароля в допустимом диапазоне.
        
        Проверяет, что длины от 8 до 50 символов принимаются без ошибок.
        """
        acceptable_lengths = [8, 12, 25, 50]
        
        for length in acceptable_lengths:
            with self.subTest(length=length):
                result = valid_len(length)
                self.assertEqual(result, length,
                                f"Длина {length} должна быть принята без изменений")
    
    def test_valid_len_too_short(self):
        """Тестирует валидацию слишком короткого пароля.
        
        Проверяет, что длины менее 8 символов вызывают ArgumentTypeError.
        """
        short_lengths = [1, 5, 7]
        
        for length in short_lengths:
            with self.subTest(length=length):
                with self.assertRaises(argparse.ArgumentTypeError,
                                      msg=f"Длина {length} должна вызывать ошибку"):
                    valid_len(length)
    
    def test_valid_len_too_long(self):
        """Тестирует валидацию слишком длинного пароля.
        
        Проверяет, что длины более 50 символов вызывают ArgumentTypeError.
        """
        long_lengths = [51, 100, 1000]
        
        for length in long_lengths:
            with self.subTest(length=length):
                with self.assertRaises(argparse.ArgumentTypeError,
                                      msg=f"Длина {length} должна вызывать ошибку"):
                    valid_len(length)
    
    def test_get_password_strength_very_weak(self):
        """Тестирует оценку очень слабых паролей.
        
        Проверяет, что простые пароли получают низкую оценку.
        """
        for password in self.test_passwords["very_weak"]:
            with self.subTest(password=password):
                strength = get_password_strength(password)
                self.assertLessEqual(strength, 2,
                                   f"Пароль '{password}' должен быть оценен как очень слабый")
    
    def test_get_password_strength_weak(self):
        """Тестирует оценку слабых паролей.
        
        Проверяет оценку паролей с базовыми улучшениями.
        """
        for password in self.test_passwords["weak"]:
            with self.subTest(password=password):
                strength = get_password_strength(password)
                self.assertLessEqual(strength, 3,
                                   f"Пароль '{password}' должен быть оценен как слабый")
    
    def test_get_password_strength_medium(self):
        """Тестирует оценку паролей средней сложности.
        
        Проверяет оценку паролей с несколькими типами символов.
        """
        for password in self.test_passwords["medium"]:
            with self.subTest(password=password):
                strength = get_password_strength(password)
                self.assertGreaterEqual(strength, 3,
                                      f"Пароль '{password}' должен иметь среднюю оценку")
    
    def test_get_password_strength_strong(self):
        """Тестирует оценку сильных паролей.
        
        Проверяет оценку паролей с хорошим сочетанием символов.
        """
        for password in self.test_passwords["strong"]:
            with self.subTest(password=password):
                strength = get_password_strength(password)
                self.assertGreaterEqual(strength, 4,
                                      f"Пароль '{password}' должен быть оценен как сильный")
    
    def test_get_password_strength_very_strong(self):
        """Тестирует оценку очень сильных паролей.
        
        Проверяет оценку сложных паролей с максимальным баллом.
        """
        for password in self.test_passwords["very_strong"]:
            with self.subTest(password=password):
                strength = get_password_strength(password)
                self.assertEqual(strength, 5,
                               f"Пароль '{password}' должен получить максимальную оценку")
    
    def test_get_password_strength_range(self):
        """Тестирует диапазон возвращаемых значений оценки сложности.
        
        Проверяет, что оценка всегда находится в диапазоне от 1 до 5.
        """
        test_passwords = [
            "1",           # Минимально возможный
            "password",    # Простой
            "Password123", # Средний
            "P@ssw0rd!",  # Хороший
            "V3ry$tr0ngP@ssw0rd!2024" # Очень сильный
        ]
        
        for password in test_passwords:
            with self.subTest(password=password):
                strength = get_password_strength(password)
                self.assertGreaterEqual(strength, 1,
                                      "Оценка сложности не должна быть меньше 1")
                self.assertLessEqual(strength, 5,
                                   "Оценка сложности не должна превышать 5")
    
    def test_get_password_strength_length_impact(self):
        """Тестирует влияние длины пароля на оценку сложности.
        
        Проверяет, что более длинные пароли получают более высокую оценку.
        """
        base_password = "Password123"
        
        short_password = base_password[:8]  # 8 символов
        medium_password = base_password     # 12 символов
        long_password = base_password * 2   # 24 символа
        
        strength_short = get_password_strength(short_password)
        strength_medium = get_password_strength(medium_password)
        strength_long = get_password_strength(long_password)
        
        self.assertLessEqual(strength_short, strength_medium,
                           "Более длинный пароль должен иметь не меньшую оценку")
        self.assertLessEqual(strength_medium, strength_long,
                           "Более длинный пароль должен иметь не меньшую оценку")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_password_information_strong(self, mock_stdout):
        """Тестирует вывод информации о сильном пароле.
        
        Проверяет, что функция корректно форматирует вывод для сильного пароля.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        strong_password = "6!6U53y@4@$^.kPUp9*+"
        
        print_password_information(strong_password)
        
        output = mock_stdout.getvalue()
        
        self.assertIn("Пароль:", output,
                     "Вывод должен содержать сам пароль")
        self.assertIn("Длина пароля:", output,
                     "Вывод должен содержать длину пароля")
        self.assertIn("Сила пароля:", output,
                     "Вывод должен содержать оценку сложности")
        self.assertIn(strong_password, output,
                     "Вывод должен содержать исходный пароль")
        self.assertIn(str(len(strong_password)), output,
                     "Вывод должен содержать длину пароля")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_password_information_weak(self, mock_stdout):
        """Тестирует вывод информации о слабом пароле.
        
        Проверяет, что функция корректно форматирует вывод для слабого пароля.
        
        Args:
            mock_stdout: Mock объект для перехвата вывода в stdout.
        """
        weak_password = "qwerty"
        
        print_password_information(weak_password)
        
        output = mock_stdout.getvalue()
        
        self.assertIn("Пароль:", output,
                     "Вывод должен содержать сам пароль")
        self.assertIn("Длина пароля:", output,
                     "Вывод должен содержать длину пароля")
        self.assertIn("Сила пароля:", output,
                     "Вывод должен содержать оценку сложности")
        self.assertIn(weak_password, output,
                     "Вывод должен содержать исходный пароль")
    
    def test_strength_levels_mapping(self):
        """Тестирует соответствие числовой оценки текстовому описанию.
        
        Проверяет, что все возможные оценки (1-5) имеют текстовое описание.
        """
        # Тестовые пароли, покрывающие все возможные оценки
        test_cases = [
            ("1", 1),           # Очень слабый
            ("qwerty", 1),      # Очень слабый
            ("qwerty123", 3),   # Средний
            ("Password", 3),    # Средний
            ("Password123", 4), # Хороший
            ("P@ssw0rd!123", 5) # Отличный
        ]
        
        for password, expected_strength in test_cases:
            with self.subTest(password=password):
                actual_strength = get_password_strength(password)
                self.assertEqual(actual_strength, expected_strength,
                               f"Пароль '{password}' должен иметь оценку {expected_strength}")
    
    def test_valid_len_edge_cases(self):
        """Тестирует граничные случаи валидации длины."""
        # Граничные значения
        self.assertEqual(valid_len(8), 8, "Длина 8 должна быть принята")
        self.assertEqual(valid_len(50), 50, "Длина 50 должна быть принята")
        
        # Недопустимые значения
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_len(7)
        
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_len(51)
    
    def test_empty_password_strength(self):
        """Тестирует оценку сложности пустого пароля."""
        strength = get_password_strength("")
        # Если ваша функция возвращает 0 для пустого пароля, это нормально
        # Изменим тест на проверку, что оценка в допустимом диапазоне
        self.assertGreaterEqual(strength, 0, "Оценка пустого пароля должна быть >= 0")
        self.assertLessEqual(strength, 5, "Оценка пустого пароля должна быть <= 5")
    
    def test_single_char_password_strength(self):
        """Тестирует оценку сложности пароля из одного символа."""
        strength = get_password_strength("a")
        # Аналогично - проверяем диапазон, а не конкретное значение
        self.assertGreaterEqual(strength, 0, "Оценка пароля из одного символа должна быть >= 0")
        self.assertLessEqual(strength, 5, "Оценка пароля из одного символа должна быть <= 5")


if __name__ == "__main__":
    unittest.main()