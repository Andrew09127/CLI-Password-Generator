import argparse

def valid_len(length):
    if length < 8:
        raise argparse.ArgumentTypeError("Пароль должен быть не менее 8 символов")
    if length > 50:
        raise argparse.ArgumentTypeError("Пароль должен быть не более 50 символов")
    return length

def get_password_strength(password):
    score = 0
    
    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(not c.isalnum() for c in password): score += 2
    
    return min(score, 5)

def print_password_information(password):
    strength = get_password_strength(password)
    strength_levels = ["Очень слабый", "Слабый", "Средний", "Хороший", "Отличный"]
    
    print(f"Пароль: {password}")
    print(f"Длина пароля: {len(password)}")
    print(f"Сила пароля: {strength_levels[strength - 1]} ({strength}/5)")