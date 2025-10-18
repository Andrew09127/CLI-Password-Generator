import random
import string

class PasswordGenerator():
    def __init__(self):
        self.chars_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
        
    def generate(self, length=12, use_uppercase=True, use_degits=True, use_special=True):
        chars = self.chars_sets['lowercase']
        
        if use_uppercase:
            chars += self.chars_sets['uppercase']
        if use_degits:
            chars += self.chars_sets['digits']
        if use_special:
            chars += self.chars_sets['special']
            
            
        password = []
        
        if use_uppercase:
            password.append(random.choice(self.chars_sets['uppercase']))
        if use_degits:
            password.append(random.choice(self.chars_sets['digits']))
        if use_special:
            password.append(random.choice(self.chars_sets['special']))   
            
        remaining_length = length - len(password)
        password.extend(random.choice(chars) for _ in range(remaining_length))
        
        random.shuffle(password)
        return ''.join(password)
        