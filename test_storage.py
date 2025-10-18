import os
import json
from storage import PasswordStorage


def cleanup_storage_files(): #Удаляем тестовые файлы если они есть
    test_files = ['test_passwords.json', 'passwords.json']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            
            
def test_storage_inicialization():
    print("Тест инициаизации хранилища")
    
    try:
        storage = PasswordStorage('test_passwords.json')
        print("Хранилище успешно инициализированно")
        return storage
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        return None
    
    
def test_password_hash():
    print("Тест хеширования паролей")
    
    storage = PasswordStorage('test_passwords.json')
    
    password = "my_secret_password" #Тест хеширования
    hash_1 = storage._hash_password(password)
    hash_2 = storage._hash_password(password)
    
    print(f"Пароль: {password}")
    print(f"Хэш 1: {hash_1}")
    print(f"Хэш 2: {hash_2}")
    
    if hash_1 == hash_2:
        print("Хеширование успешноБ пароли одинаковые")
    else:
        print("Хеширование не удалось")
        
    different_password = "different_password"
    hash_3 = storage._hash_password(different_password)
    
    
    if hash_1 != hash_3:
        print("Разные пароли дают разные хеши (все успешно)")
    else:
        print("Разные пароли дают одинаковые хеши")
        

def test_store_and_verify_password(): #Тест проверки и сохранения паролей
    print("Тест проверки и сохранения паролей")
    
    storage = PasswordStorage('test_passwords.json')
    
    #Тестовые данные
    service = "Yandex"
    username = "padalkoandrej@yandex.ru"
    password = "qwerty2005"
    master_password = "MyMasterPassword"
    
    
    try:
        storage.store_password(service, username, password, master_password)
        print("Проль успешно сохранен")
        
        if storage.verify_password(service, password, master_password): #Проверяем правильный пароль
            print("Правилльный Пароль подтвержден!")
        else:
            print("Правилльный Пароль НЕ подтвержден!")
            
        wrong_password = "wrong_password" #Проверяем НЕ правильный пароль
        if not storage.verify_password(service, wrong_password, master_password):
            print("Неправильный пароль отклонен")
        else:
            print("Неправильный пароль принят")
            
        wrong_master = "WrongMaster"
        if not storage.verify_password(service, password, wrong_password):
            print("Неправильный мастер пароль отклонен")
        else:
            print("Неправильный мастер пароль принят")
        
    except Exception as e:
        print(f"Ошибка при сохранении или проверке: {e}")
        

def test_multiple_services(): #Тест работы с несколькими сервисами
    print("Тест работы с несколькими сервисами")
    
    
    storage = PasswordStorage('test_passwords.json')
    master_password = "MyMasterPassword"
    
    services = [
    ("github", "Andrew09127", "GitHubPassQwerty!"),
    ("yandex", "padalkoandrej@yandex.ru", "YandexPass456!"),
    ("Kiinopoisk", "ANDREY_KINOPOISK", "QWERTY09127")
    ]
    
    
    try:
        for service, username, password in services:
            storage.store_password(service, username, password, master_password)
            print(f"Сервис '{service}' успешно сохранен!")
            
        print("Поиск сервисов")
        results = storage.find_service("git")
        if results and "github" in results:
            print("Поиск по части имени работает")
        else:
            print("Поиск по части имени не работает")
            
        results = storage.find_service("DSTU.ru")
        if not results:
            print("Поиск несуществующего сервиса возвращает пустой результат")
        else:
            print("Поиск несуществующего сервиса возвращает данные")
            
    except Ellipsis as e:
        print(f"Ошибка при работе с несколькими сервисами: {e}")
        