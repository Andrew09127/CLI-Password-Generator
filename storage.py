"""Модуль работы с защищенным хранилищем паролей.

Обеспечивает безопасное сохранение, загрузку и проверку паролей 
с использованием хеширования и мастер-пароля.
"""

import hashlib
import json
import os
from getpass import getpass

class PasswordStorage():
    """Класс для безопасного хранения паролей с мастер-паролем."""
    def __init__(self, storage_file='passwords.json'):
        """Инициализирует хранилище паролей.
        
        Args:
            storage_file (str): Путь к файлу для хранения паролей. 
                               По умолчанию 'passwords.json'.
        """
        self.storage_file = storage_file
        self.data = self._load_data()
        
    def _load_data(self):
        """Загружает данные из файла хранилища.
        
        Returns:
            dict: Загруженные данные или пустой словарь, если файл не существует.
        """
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_data(self):
        """Сохраняет данные в файл хранилища."""
        with open(self.storage_file, 'w') as f:
            json.dump(self.data, f, indent=2)
            
    def _hash_password(self, password):
        """Хеширует пароль с использованием SHA-256.
        
        Args:
            password (str): Пароль для хеширования.
        
        Returns:
            str: Хеш пароля в шестнадцатеричном формате.
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def store_password(self, service, username, password, master_password): #Хешируем мастер-пароль для проверки
        """Сохраняет пароль для указанного сервиса.
        
        Args:
            service (str): Название сервиса.
            username (str): Имя пользователя.
            password (str): Пароль для сохранения.
            master_password (str): Мастер-пароль для доступа к хранилищу.
        
        Raises:
            ValueError: Если мастер-пароль неверен.
        """
        master_hash = self._hash_password(master_password)
        
        if 'master_hash' not in self.data:
            self.data['master_hash'] = master_hash
        elif self.data['master_hash'] != master_hash:
            raise ValueError("Неверный мастер-пароль")
        
        password_hash = self._hash_password(password) #Хешируем и сохраняем пароль
        
        if 'passwords' not in self.data:
            self.data['passwords'] = {}
            
        self.data['passwords'][service] = {
            'username': username,
            'password_hash': password_hash
        }
        
        self._save_data()
        
    
    def verify_password(self, service, password, master_password):
        """Проверяет правильность пароля для указанного сервиса.
        
        Args:
            service (str): Название сервиса.
            password (str): Пароль для проверки.
            master_password (str): Мастер-пароль для доступа к хранилищу.
        
        Returns:
            bool: True если пароль верный, False в противном случае.
        """
        master_hash = self._hash_password(master_password)
        if self.data.get('master_hash') != master_hash:
            return False
        
        stored_hash = self.data['passwords'].get(service, {}).get('password_hash')
        return stored_hash == self._hash_password(password)
    
    def find_service(self, service_name):
        """Находит сервисы по частичному совпадению названия.
        
        Args:
            service_name (str): Название сервиса или его часть для поиска.
        
        Returns:
            dict: Словарь найденных сервисов, где ключ - полное название, 
                  значение - данные сервиса.
        """
        return {k: v for k, v in self.data.get('passwords', {}).items()
                if service_name.lower() in k.lower()}