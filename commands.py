from generator import PasswordGenerator
from storage import PasswordStorage
from utils import print_password_information
from getpass import getpass

class PasswordCommands:
    def __init__(self):
        self.generator = PasswordGenerator()
        self.storage = PasswordStorage()
        
    def generate_command(self, args):
        password = self.generator.generate(
            length=args.length,
            use_uppercase=args.uppercase,
            use_digits=args.digits,
            use_special=args.special
        )
        
        print_password_information(password)
        
        
        if args.save:        
            service = input("Введите название сервиса: ")            
            username = input("Введите имя пользователя: ")
            master_password = getpass("Введите мастер-пароль: ")
            
            try:
                self.storage.store_password(service, username, password, master_password)
                print(f"Пароль для {service} сохранен!")
            except ValueError as e:
                print(f"Ошибка сохранения: {e}")
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
            
    def find_command(self, args):
        service_name = args.service
        results = self.storage.find_service(service_name)
        
        
        if results:
            print(f"Найдено {len(results)} сервисов:")
            for service, data in results.items():
                print(f"  {service}: {data['username']}")
        else:
            print("Сервисы не найдены")
            
        
    def verify_command(self, args):
        service = args.service
        password = getpass("Введите пароль для проверки: ")
        master_password = getpass("Введите мастер-пароль: ")
        
        
        try:
            if self.storage.verify_password(service, password, master_password):
                print("Пароль верный!")
            else:
                print("Пароль неверный!")
        except Exception as e:
            print(f"Ошибка проверки: {e}")