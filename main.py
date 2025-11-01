"""Основной модуль CLI Password Generator.

Этот модуль предоставляет интерфейс командной строки для генерации паролей,
их сохранения и управления через различные команды.
"""

import argparse
from commands import PasswordCommands


def main():
    """Точка входа в приложение.
    
    Обрабатывает аргументы командной строки и выполняет соответствующие команды.
    
    Raises:
        SystemExit: При завершении работы приложения.
    """
    
    parser = argparse.ArgumentParser(description='CLI Password Generator - генератор и менеджер паролей')
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    #Команда генерации
    gen_parser = subparsers.add_parser('generate', help='Сгенерировать пароль')
    gen_parser.add_argument('-l', '--length', type=int, default=12, help='Длина пароля (по умолчанию 12)')
    gen_parser.add_argument('--no-uppercase', dest='uppercase', action='store_false', help='Без заглавных букв')
    gen_parser.add_argument('--no-digits', dest='digits', action='store_false', help='Без цифр')
    gen_parser.add_argument('--no-special', dest='special', action='store_false', help='Без спец символов')
    gen_parser.add_argument('--save', action='store_true', help='Сохранить пароль в хранилище')
    
    
    #Команда поиска
    find_parser = subparsers.add_parser('find', help='Найти сервис')
    find_parser.add_argument('service', help='Название сервиса для поиска')
    
    #Команда проверки
    verify_parser = subparsers.add_parser('verify', help='Проверить пароль')
    verify_parser.add_argument('service', help='Название сервиса')
    
    
    args = parser.parse_args()
    commands = PasswordCommands()
    
    
    if args.command == 'generate':
        commands.generate_command(args)
    elif args.command == 'find':
        commands.find_command(args)
    elif args.command == 'verify':
        commands.verify_command(args)
    else:
        parser.print_help()
    
if __name__== '__main__':
    main()
        