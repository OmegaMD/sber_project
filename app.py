# imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import hashlib
import hmac
import json

import settings

# enumerators
from enum import Enum

# device type enum
class DeviceType(Enum):
    UNKNOWN = 0
    MOBILE = 1
    COMPUTER = 2

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

        # device type
        self.device_type = DeviceType.UNKNOWN

        # base directory for templates (htmls)
        self.base_dir = ''

        ### flask callback functions ###

        # home flask function
        @self.flask.route('/')
        def home():
            # getting browser info
            user_agent = request.headers.get('User-Agent')

            if "Mobile" in user_agent:
                self.device_type = DeviceType.MOBILE
                self.base_dir = 'mobile/'
            else:
                self.device_type = DeviceType.COMPUTER
                self.base_dir = 'computer/'

            return render_template(self.base_dir + 'index.html')

        # going to login flask function
        @self.flask.route('/login', methods=['GET'])
        def login():
            #print("Login page")
            print(self.base_dir + 'login.html')
            return render_template(self.base_dir + 'login.html')

        @self.flask.route('/submit_login', methods=['POST'])
        def submit_login():
            #print(f"login:    { str(request.form.get('login_input')) }")
            #print(f"password: { str(request.form.get('password_input')) }")
            return render_template(self.base_dir + 'map.html')

        # API token and secret for Telegram login
        self.API_TOKEN = settings.API_TOKEN       

        # URL для проверки авторизации
        self.TELEGRAM_API_URL = 'https://api.telegram.org/bot' + self.API_TOKEN + '/getMe'
        self.SECRET_KEY = settings.SECRET_KEY

        # Route for Telegram login verification
        @self.flask.route('/login_check', methods=['GET'])
        def login_check():
            # Получаем параметры из запроса
            data = request.args
            #print("Received data:", data)

            telegram_id = data.get('id')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            username = data.get('username', '')
            signature = data.get('hash')
            
            return render_template(self.base_dir + 'map.html')
            '''return jsonify({"status": "success", "user_info": {
                    "id": telegram_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username
                }})'''

# application instance
app = App()

# application entry point for local debug
if __name__ == '__main__':
    app.run()

