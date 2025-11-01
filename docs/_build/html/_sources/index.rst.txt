.. CLI PASSWORD GENERATOR documentation master file, created by
   sphinx-quickstart on Sat Nov  1 15:38:36 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CLI Password Generator Documentation
====================================

Документация для проекта **CLI Password Generator** - генератора и менеджера паролей.

Описание проекта
----------------

CLI Password Generator - это консольное приложение для генерации безопасных паролей
и их хранения с использованием мастер-пароля.

Быстрый старт
-------------

.. code-block:: bash

   python main.py generate --length 12 --save
   python main.py find gmail
   python main.py verify github

Модули проекта
--------------

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   modules

Основные функции
----------------

- **Генерация паролей** с настраиваемыми параметрами
- **Безопасное хранение** с хешированием паролей
- **Поиск паролей** по названию сервиса
- **Проверка сложности** паролей

Индекс и поиск
==============

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`