from utils import valid_len, get_password_strength, print_password_information

def test_utils():
    print("Тест утилиты для оценки пароля")
    try:
        print("Тест валидации длины:")
        length_1 = valid_len(12)
        print(f"Валидация длины 12: {length_1}")
        
        length_2 = valid_len(7)
        print(f"Валидация длины 7: {length_2}")
    except Exception as e:
        print(f"Валидация длины 7: {e}")
        
    try:
        length_3 = valid_len(70)
        print(f"Валидация длины 70: {length_3}")
    except Exception as e:
        print(f"Валидация длины 70: {e}")
    print()
    
    print("Оценка сложности пароля")        
    test_password = {
        "123",
        "qwerty",
        "password",
        "&2;],]EG_z:a",
        "k:Cz+2J6",
        "qixHOQdHUeTW",
        "$g3&29(2;h9:",
        "6!6U53y@4@$^.kPUp9*+"
    } #Пароли взяты после теста test_generator
    
    for i in test_password:
        strength = get_password_strength(i)
        print(f"'{i}' -> сила пароля: {strength}/5")
    print()
    
    print("Вывод инфы о пароле")
    print_password_information("6!6U53y@4@$^.kPUp9*+")
    print()
    print_password_information("qwerty")
    
def test_interactive(): #интерактивное тестирование
    print("Интерактивное тестирование")
    
    while True:
        print("Введите пароль для проверки надежности (или 'quit' для выхода):")
        password = input("> ")
        
        if password.lower() == 'quit':
            break
        
        print_password_information(password)
if __name__== "__main__":
    test_utils()
    test_interactive()