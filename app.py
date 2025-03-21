# imports
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import requests
#import hashlib
#import hmac
import json
import pickle

import settings

from database import Database

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

    # session variable updating function
    def set_var(self, name, value):
        session[name] = value
    
    # getting session variable value function
    def get_var(self, name):
        if name in session:
            return session[name]
        return None

    # class initialization function
    def __init__(self):
        ### local class variables ###

        # flask
        self.flask = Flask(__name__)

        # device type
        # self.device_type = DeviceType.UNKNOWN

        # base directory for templates (htmls)
        # self.base_dir = 'computer/'

        ### flask variables setup ###
        self.flask.secret_key = 'GiantAlienDildo'

        # API token and secret for Telegram login
        self.API_TOKEN = settings.API_TOKEN       

        # URL для проверки авторизации
        self.TELEGRAM_API_URL = 'https://api.telegram.org/bot' + self.API_TOKEN + '/getMe'
        self.SECRET_KEY = settings.SECRET_KEY

        ### database ###
        
        self.database = Database('database.db')

        ### 2gis api key ###
        self.TWOGIS_API_KEY = 'ab7b70c9-9132-468f-8b4c-87177a2418cf'

        ### flask callback functions ###

        # home flask function
        @self.flask.route('/')
        def home():
            # user info setup
            # self.set_var("user", self.database.access_user("guest"))
            session["user"] = pickle.dumps(self.database.access_user("guest"))

            # getting browser info
            user_agent = request.headers.get('User-Agent')
            print("nigga0")
            return render_template('map.html')


        @self.flask.route('/cafes/<float:lat>/<float:lon>')
        def get_cafes(lat, lon):
            print('nigga2')
            url = f"https://catalog.api.2gis.com/3.0/items"
            params = {
                'key': self.TWOGIS_API_KEY,
                'point': f"{lon},{lat}",
                'radius': 1000,  # радиус поиска в метрах
                'q': 'кафе',
                'limit': 10,
                'fields': 'items.point'
            }
            response = requests.get(url, params=params)

            if response.status_code != 200:
                return jsonify({"error": "Failed to fetch data from 2GIS"}), 500

            data = response.json()

            cafes = []
            if 'result' in data:
                for item in data['result']['items']:
                    cafes.append({
                        'name': item['name'],
                        'address': item['address_name'],
                        'point': item['point']
                    })

            print(cafes)
            
            return jsonify(cafes)

        @self.flask.route('/main_page', methods=['POST'])
        def main():
            print(pickle.loads(self.get_var("user")))
            return render_template('home.html',
                                   user=pickle.loads(self.get_var("user")),
                                   top_discount_partners=self.database.access_top_discount_partners())

# application instance
app = App()

# application entry point for local debug
if __name__ == '__main__':
    app.run()