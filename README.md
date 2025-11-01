# 🔐 CLI Password Generator

**Генератор безопасных паролей с защищенным хранилищем** - консольная утилита для создания, хранения и управления паролями с русскоязычным интерфейсом.

## ✨ Возможности

-  **Генерация безопасных паролей** с настраиваемой длиной и набором символов
-  **Защищенное хранение** паролей с использованием мастер-пароля
-  **Поиск сервисов** по названию или части имени
-  **Проверка паролей** на соответствие сохраненным
-  **Оценка сложности** пароля

## Документация
Документирование кода
Проект полностью задокументирован в соответствии с стандартом Google docstrings. Документация включает:

- Модульные докстринги для всех файлов

- Документацию для всех классов и методов

- Описания параметров, возвращаемых значений и исключений

## Генерация HTML документации с помощью Sphinx
Установка Sphinx
```bash 
pip install sphinx sphinx-rtd-theme
```

### Генерация документации

```bash
# Перейдите в папку docs
cd docs

# Сгенерируйте HTML документацию
.\make html

# Или альтернативная команда
sphinx-build -b html . _build/html
```

## Запуск локального сервера для просмотра документации

После генерации документации запустите локальный сервер:
```bash
# Перейдите в папку с сгенерированной документацией
cd _build/html

# Запустите сервер на порту 8800
python -m http.server 8800 --bind 127.0.0.1
```

Откройте в браузере: http://localhost:8800
## 🚀 Установка и запуск

## Установка

### Установите зависимости для документации:
```bash
pip install -r requirements.txt
```

### 📥 Скачивание проекта

```bash
# Клонируйте репозиторий
git clone https://github.com/Andrew09127/CLI-Password-Generator.git

Или скачайте ZIP архив с GitHub и распакуйте его
```
## 📁 Настройка проекта
```bash
# Перейдите в папку проекта
cd "CLI Password Generator"

# Проверьте, что все файлы на месте
dir
# или
ls
```

## ▶️ Первый запуск
```bash
# Проверьте, что проект работает
python main.py --help

# Должна появиться справка по использованию
```
## 🚀 Быстрый старт

```bash
# Сгенерировать пароль
python main.py generate

# Сгенерировать и сохранить пароль
python main.py generate --save

# Найти сервис
python main.py find gmail

# Проверить пароль
python main.py verify github
```
## Генерация паролей
```bash
# Базовая генерация
python main.py generate
python main.py generate --length 16
python main.py generate -l 20

# С разными наборами символов
python main.py generate --no-uppercase    # Без заглавных букв
python main.py generate --no-digits       # Без цифр
python main.py generate --no-special      # Без спецсимволов

# Сохранение
python main.py generate --save
python main.py generate --length 14 --no-special --save
```

## Поиск и проверка
```bash
# Поиск сервисов
python main.py find gmail
python main.py find mail
python main.py find git

# Проверка пароля
python main.py verify github
```

## Справка
```bash
python main.py -h
python main.py generate -h
python main.py find -h
python main.py verify -h
```

## 🗝️ Система мастер-пароля
Мастер-пароль создается один раз и используется для всех операций с файлом!
```bash
# Первое использование - устанавливаем мастер-пароль
python main.py generate --save
# Вводим: master_password = "secret123"

# Все последующие операции
python main.py generate --save
# Вводим: master_password = "secret123"  

python main.py verify gmail
# Вводим: master_password = "secret123"  
```

## 🔒 Безопасность
- Пароли хэшируются (SHA-256)
  
- Невозможно восстановить пароли из файла
  
- Защита мастер-паролем
  
-  Не хранятся в открытом виде
  
## Стурктура проекта

CLI Password Generator/
```bash
├── docs #Генерация документации
├── main.py # Основной CLI интерфейс
├── commands.py # Обработчики команд
├── generator.py # Логика генерации паролей
├── storage.py # Система хранения паролей
├── utils.py # Вспомогательные функции
├── test_commands.py # Тесты команд
├── test_generator.py # Тесты генератора
├── test_storage.py # Тесты хранилища
├── test_integration.py # Интеграционные тесты
├── README.md # Документация
└── passwords.json # Файл с паролями (создается автоматически)
```

## 👨‍💻 Автор
**Андрей Падалко ВКБ32**  
📧 Email: padalkoandrej50@gmail.com  
🐙 GitHub: [Andrew09127](https://github.com/Andrew09127)