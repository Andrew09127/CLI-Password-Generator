from generator import PasswordGenerator

def test_generator():
    print("Тест генерации паролей")
    
    generator = PasswordGenerator()
    
    # Тест 1: Генерация пароля по умолчанию
    print("1. дефолтный пароль:")
    password1 = generator.generate()
    print(f"   Password: {password1}")
    print(f"   Length: {len(password1)}")
    print()
    
    # Тест 2: Короткий пароль
    print("2. короткий пароль (8 chars):")
    password2 = generator.generate(length=8)
    print(f"   Password: {password2}")
    print(f"   Length: {len(password2)}")
    print()
    
    # Тест 3: Пароль только с буквами
    print("3. только буквы:")
    password3 = generator.generate(use_digits=False, use_special=False)
    print(f"   Password: {password3}")
    print(f"   Contains digits: {any(c.isdigit() for c in password3)}")
    print(f"   Contains special: {any(not c.isalnum() for c in password3)}")
    print()
    
    # Тест 4: Пароль без заглавных букв
    print("4. Без заглавных букв:")
    password4 = generator.generate(use_uppercase=False)
    print(f"   Password: {password4}")
    print(f"   Contains uppercase: {any(c.isupper() for c in password4)}")
    print()
    
    # Тест 5: Длинный пароль со всеми символами
    print("5. длинный пароль со всеми символами:")
    password5 = generator.generate(length=20, use_uppercase=True, use_digits=True, use_special=True)
    print(f"   Password: {password5}")
    print(f"   Length: {len(password5)}")
    print(f"   Has uppercase: {any(c.isupper() for c in password5)}")
    print(f"   Has digits: {any(c.isdigit() for c in password5)}")
    print(f"   Has special: {any(not c.isalnum() for c in password5)}")

if __name__ == "__main__":
    test_generator()