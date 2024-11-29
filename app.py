# imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import hashlib
import hmac
import json

import settings


# application class
class App:
    # application starting function
    def run(self):
        self.flask.run(debug=True)

    # class initialization function
    def __init__(self):
        ### local class variables ###

        # flask
        self.flask = Flask(__name__)

        ### flask callback functions ###

        # home flask function
        @self.flask.route('/')
        def home():
            return render_template('index.html')

        # going to login flask function
        @self.flask.route('/login', methods=['GET'])
        def login():
            print(832489231843291)
            return render_template('login.html')

        @self.flask.route('/submit_login', methods=['POST'])
        def submit_login():
            #print(f"login:    { str(request.form.get('login_input')) }")
            #print(f"password: { str(request.form.get('password_input')) }")
            return render_template('map.html')

        # API token and secret for Telegram login
        self.API_TOKEN = settings.API_TOKEN
        

        # URL для проверки авторизации
        self.TELEGRAM_API_URL = 'https://api.telegram.org/bot' + self.API_TOKEN + '/getMe'

        self.SECRET_KEY = settings.SECRET_KEY



        # Route for Telegram login verification
        @self.flask.route('/login_check', methods=['GET'])
        def login_check():
            # Получаем параметры из запроса
            print(12312321313)
            data = request.args
            print("Received data:", data)

            telegram_id = data.get('id')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            username = data.get('username', '')
            signature = data.get('hash')
            # Проверяем подпись

            if self.check_signature(data, signature):
                # Авторизация успешна
                return jsonify({"status": "success", "user_info": {
                    "id": telegram_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username
                }})
            else:
                return jsonify({"status": "error", "message": "Invalid signature"}), 400

        # Функция для проверки подписи Telegram
        def check_signature(self, data, signature):
            # Собираем строку из данных в правильном порядке для подписи
            secret = bytes(self.SECRET_KEY, 'utf-8')

            # Строка данных для подписи — это то, что Telegram передает.
            # Мы создаем строку из параметров запроса в нужном порядке.
            string_data = ''.join(f"{key}={data[key]}" for key in sorted(data.keys()))

            # Генерируем подпись
            generated_signature = hmac.new(secret, string_data.encode('utf-8'), hashlib.sha256).hexdigest()

            return generated_signature == signature

# создание экземпляра приложения
app = App()
print(1, 2, 3, 4)
# application entry point for local debug
if __name__ == '__main__':
    app.run()

