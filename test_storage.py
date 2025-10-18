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
        if not storage.verify_password(service, password, wrong_master):
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
            
        results = storage.find_service("DSTU.ru") # Поиск несуществующего сервиса
        if not results:
            print("Поиск несуществующего сервиса возвращает пустой результат")
        else:
            print("Поиск несуществующего сервиса возвращает данные")
            
    except Exception as e:
        print(f"Ошибка при работе с несколькими сервисами: {e}")
        
def test_wrong_master_password(): #Тест неправильного мастер-пароля
    print("Тест неправильного мастер-пароля")
    
    storage = PasswordStorage('test_passwords.json')
    
    try:
        storage.store_password("test", "user", "pass", "wrong_master") #1 сохранение устанавливает мастер-пароль
        
        #Попытка сохранить с неправильным мастер-паролем        
        try:
            storage.store_password("test2", "user2", "pass2", "wrong_master")
            print("Неправильный мастер-пароль был принят")
        except ValueError as e:
            print(f"Неправильный мастер-пароль был отколнен: {e}")
            
    except Exception as e:
        print(f"Ошибка в тесте мастер-пароля: {e}")
        
        
def test_file_persistence(): #тест сохранения в файл
    print("тест сохранения в файл")
    
    filename = 'test_persistence.json'
    
    storage_1 = PasswordStorage(filename) #Создаем 1 хранилище и сохраняем туда данные
    storage_1.store_password("persistent", "user", "password", "master")
    
    storage_2 = PasswordStorage(filename) #Создаем 2 хранилищеБ должны загрузиться данные из файла
    
    if storage_2.verify_password("persistent", "password", "master"): #Проверяем что данные сохранились
        print("Данные успешно сохранились в файл и загрузились")
    else:
        print("Данные не сохранились в файл")
        
        
def test_data_structure(): #Тест структуры данных в файл
    print("Тест структуры данных в файл")
    
    filename = 'test_passwords.json'
    storage = PasswordStorage(filename)
    
    storage.store_password("test_service", "test_user", "test_pass", "master_pass")
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
        print("Структура данных в файле:")
        print(f"Есть master_hash: {'master_hash' in data}")
        print(f"Есть passwords: {'passwords' in data}")
        
        if 'passwords' in data and 'test_service' in data['passwords']:
            service_data = data['passwords']['test_service']
            print(f"Данные сервиса: username={service_data.get('username')}")
            print(f"Пароль захеширован: {len(service_data.get('password_hash', '')) == 64}")
            print("Структура данных корректна")
        else:
            print("Структура данных некорректна")
            
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        
        
def interactive_test():
    print("Интерактивный тест")
    
    storage = PasswordStorage('passwords.json')
    
    while True:
        print("\nВыберите действие:")
        print("1 - Сохранить пароль")
        print("2 - Найти сервис") 
        print("3 - Проверить пароль")
        print("0 - Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            service = input("Сервис: ")
            username = input("Имя пользователя: ")
            password = input("Пароль: ")
            master_password = input("Мастер-пароль: ")
            
            try:
                storage.store_password(service, username, password, master_password)
                print("Пароль сохранен!")
            except Exception as e:
                print(f"Ошибка: {e}")
                
                
        elif choice == "2":
            service_name = input("Название сервиса для поиска: ")
            result = storage.find_service(service_name)
            
            if result:
                print("найдены сервисы:")
                for service, data in result.items():
                    print(f"{service}: {data['username']}")
            else:
                print("Сервисы не найдены")
                    
                    
        elif choice == "3":
            service = input("Сервис: ")
            password = input("Пароль для проверки: ")
            master_password = input("Мастер-пароль ")
            
            
            if storage.verify_password(service, password, master_password):
                print("Пароль верный!")
            else:
                print("Пароль неверный!")
            
            
        elif choice == "0":
            break
        else:
            print("Неверный выбор")
            
            
def run_all_tests(): #Запуск всех тестов
    print("Запуск всех тестов storage.py")
    
    cleanup_storage_files()
    test_storage_inicialization()
    
    cleanup_storage_files()
    test_password_hash()
    
    cleanup_storage_files()
    test_store_and_verify_password()
    
    cleanup_storage_files()
    test_multiple_services()
    
    cleanup_storage_files()
    test_wrong_master_password()
    
    cleanup_storage_files()
    test_file_persistence()
    
    cleanup_storage_files()
    test_data_structure()
    
    print("Все тысты завершены")
    
    
if __name__== "__main__":
    import sys     
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_test()
    else:
        run_all_tests()