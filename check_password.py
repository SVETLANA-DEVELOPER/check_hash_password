"""
Задача:
Написать программу, которая запрашивает пароль, и с помощью алгоритма sha256 вычисляет хеш.
Для генерации хеша используется криптографическая соль.
Выводит полученный хеш.

Далее запрашивает пароль повторно, снова вычисляет хеш.
Проверяет совпадают ли пароли, сравнив хеши.
"""


import hashlib
from uuid import uuid4
import mysql.connector


def check_password(psswd: str):
    # Создаем соединение с нашей базой данных
    db_connect = mysql.connector.connect(user='root', database='test_database', password='Svetlanka!4')
    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = db_connect.cursor()

    # Генерируем "соль" и формируем Хэш первого пароля
    salt = uuid4().hex
    hash_obj_1 = hashlib.sha256(salt.encode() + psswd.encode())
    hash_1 = hash_obj_1.hexdigest()
    print(f'Хэш1: {hash_1}')

    # Записываем соль и хэш в БД. Делаем INSERT запрос к базе данных, используя обычный SQL-синтаксис
    cursor.execute("INSERT INTO hashes (salt, hash) VALUES (%s, %s)", (salt, hash_1))
    # Проверка
    cursor.execute("SELECT hash FROM hashes ORDER BY id LIMIT 4")
    results = cursor.fetchall()
    print(f'В базе данных хранится строка: {results}')

    password_2 = input('Введите пароль еще раз для проверки: ')
    hash_obj_2 = hashlib.sha256(salt.encode() + password_2.encode())
    hash_2 = hash_obj_2.hexdigest()
    print(f'Хэш извлеченный из БД: {results[-1][-1]}')

    # Проверяем совпадают ли хеш первого пароля, записанный в БД и хеш второго пароля
    if results[-1][-1] == hash_2:
        print('Вы ввели ВЕРНЫЙ пароль')
    else:
        print('Вы ввели НЕВЕРНЫЙ пароль')

    # Закрываем соединение с БД
    db_connect.close()


password_1 = input('Введите пароль: ')
check_password(password_1)
