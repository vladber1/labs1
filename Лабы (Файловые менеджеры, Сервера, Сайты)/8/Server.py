# -*- coding: utf-8 -*-

import os
from flask import Flask, request
import hashlib
import datetime
import json

app = Flask(__name__)

if os.path.exists('users.json') and os.path.getsize('users.json') > 0:
    with open('users.json', 'r') as f:
        users = json.load(f)
else:
    users = []

context = ('tls-certificates/server.crt', 'ssl-keys/server.key')

reg_form_begin = '''<html><body>
<form method="post" action="/">'''
reg_form_body = '''<input type="text" name="login">
<input type="password" name="password">
<button type="submit">Зарегистрироваться</button>'''
reg_form_end = '''</form>
</body></html>'''


@app.route('/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        # обработка GET-запроса - отображение формы
        return reg_form_begin + reg_form_body + reg_form_end
    else:
        # обработка POST-запроса - сохранение данных в БД
        login = request.form['login']
        password = request.form['password']

        # Проверка поля логина
        if not login:
            return reg_form_begin + reg_form_body + '''<span>Не введен логин</span>''' + reg_form_end

        # Проверка поля пароля
        if not password:
            return reg_form_begin + reg_form_body + '''<span>Не введен пароль</span>''' + reg_form_end

        # Проверка, что пользователь уже не зарегистрирован
        user_exists = False
        for user in users:
            if user['login'] == login:
                user_exists = True
                break

        if user_exists:
            return reg_form_begin + reg_form_body + '''<span>Пользователь уже зарегистрирован</span>''' + reg_form_end

        # Хеширование пароля
        salt = 'my_salt'
        hash_object = hashlib.sha256((password + salt).encode())
        password_hash = hash_object.hexdigest()

        # Добавление пользователя
        user = {
            'login': login,
            'password_hash': password_hash,
            'registration_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        users.append(user)

        with open('users.json', 'w') as f:
            json.dump(users, f)

        print(*users, sep="\n")

        return reg_form_begin + reg_form_body + '''<span>Вы успешно зарегистрировались</span>''' + reg_form_end


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=True)
