import hashlib
import json
import os
from getpass import getpass

class PasswordStorage():
    def __init__(self, storage_file='passwords.json'):
        self.storage_file = storage_file
        self.data = self._load_data()
        
    def _load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_data(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.data, f, indent=2)
            
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def store_password(self, service, username, password, master_password): #Хешируем мастер-пароль для проверки
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
        master_hash = self._hash_password(master_password)
        if self.data.get('master_hash') != master_hash:
            return False
        
        stored_hash = self.data['passwords'].get(service, {}).get('password_hash')
        return stored_hash == self._hash_password(password)
    
    def find_service(self, service_name):
        return {k: v for k, v in self.data.get('passwords', {}).items()
                if service_name.lower() in k.lower()}