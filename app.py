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

        ### flask pages callback functions ###

        # home flask function
        @self.flask.route('/')
        def home():
            # user info setup
            # self.set_var("user", self.database.access_user("guest"))
            session["user"] = pickle.dumps(self.database.access_user("guest"))
            session["last_location_search"] = ""

            # getting browser info
            user_agent = request.headers.get('User-Agent')
            print("nigga0")
            return render_template('map.html', locations=[])

        # main page callback function
        @self.flask.route('/main_page', methods=['POST'])
        def main():
            print(pickle.loads(self.get_var("user")))
            return render_template('home.html',
                                   user=pickle.loads(self.get_var("user")),
                                   top_discount_partners=self.database.access_top_discount_partners())

        # map page flask callback function
        @self.flask.route('/map')
        def map():
            return render_template('map.html', locations=[])

        ### flask inner callback functions ###

        # user location saving function
        @self.flask.route('/save_user_location/<float:lat>/<float:lon>')
        def save_user_location(lat, lon):
            session["lat"] = lat
            session["lon"] = lon
            return "200"

        # flask location search bar callback function
        @self.flask.route('/location_search', methods=['POST'])
        def location_search():
            user_input = request.form['location_search_bar']
            session["last_location_search"] = user_input

            if user_input != '':
                locations = search_closest_locations(session['lat'], session['lon'], user_input)
                return render_template('map.html', locations=locations)
            return redirect(url_for('map'))

        ### help functions ###

        # closest locations based on query searching function
        def search_closest_locations(lat, lon, query):
            url = f"https://catalog.api.2gis.com/3.0/items"
            params = {
                'key': self.TWOGIS_API_KEY,
                'point': f"{lon},{lat}",
                # 'page_size': 30,
                'radius': 1000,  # радиус поиска в метрах
                'q': query,
                'fields': 'items.point',
                'sort': 'distance',
                # 'ype': 'adm_div.city'
            }
            response = requests.get(url, params=params)

            if response.status_code != 200:
                print('2gis error')
                return jsonify({"error": "Failed to fetch data from 2GIS"}), 500

            data = response.json()

            locations = []
            if 'result' in data:
                for item in data['result']['items']:
                    partner = self.database.access_partner(item['name'].split(',')[0])
                    locations.append({
                        'name': partner.name,
                        'address': item['address_name'],
                        'point': item['point'],
                        'img': partner.image_url,
                        'logo': partner.logo_url
                    })
            print(len(locations))
            return locations

# application instance
app = App()

# application entry point for local debug
if __name__ == '__main__':
    app.run()