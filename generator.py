"""Модуль генерации паролей.

Содержит класс PasswordGenerator для создания случайных паролей с различными параметрами.
"""

import random
import string

class PasswordGenerator():
    """Класс для генерации паролей с настраиваемыми параметрами."""
    def __init__(self):
        """Инициализирует наборы символов для генерации паролей."""
        self.chars_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
        
    def generate(self, length=12, use_uppercase=True, use_digits=True, use_special=True):
        """Генерирует случайный пароль с заданными параметрами.
        
        Гарантирует наличие хотя бы одного символа из каждого включенного типа.
        
        Args:
            length (int): Длина пароля. По умолчанию 12.
            use_uppercase (bool): Использовать заглавные буквы. По умолчанию True.
            use_digits (bool): Использовать цифры. По умолчанию True.
            use_special (bool): Использовать специальные символы. По умолчанию True.
        
        Returns:
            str: Сгенерированный пароль.
        
        Raises:
            ValueError: Если длина пароля недостаточна для включенных типов символов
                      или все типы символов отключены.
        """
        chars = self.chars_sets['lowercase']
        
        if use_uppercase:
            chars += self.chars_sets['uppercase']
        if use_digits:
            chars += self.chars_sets['digits']
        if use_special:
            chars += self.chars_sets['special']
            
            
        password = []
        
        if use_uppercase:
            password.append(random.choice(self.chars_sets['uppercase']))
        if use_digits:
            password.append(random.choice(self.chars_sets['digits']))
        if use_special:
            password.append(random.choice(self.chars_sets['special']))   
            
        remaining_length = length - len(password)
        password.extend(random.choice(chars) for _ in range(remaining_length))
        
        random.shuffle(password)
        return ''.join(password)
        