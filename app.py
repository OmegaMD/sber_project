# imports
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import requests
import pickle
import json
import datetime

import settings

# database
from database import DataBase, User, Partner, SupportChat, Support
# from database.py import *

# map and parser
from parser import Parser
import dictionary

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
        # self.flask.run(debug=True)
        self.socketio.run(self.flask)

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
        self.flask.secret_key = 'GiantAlienDildo'
        self.socketio = SocketIO(self.flask)

        # device type
        # self.device_type = DeviceType.UNKNOWN

        # base directory for templates (htmls)
        # self.base_dir = 'computer/'

        # API token and secret for Telegram login
        self.API_TOKEN = settings.API_TOKEN       

        # URL для проверки авторизации
        self.TELEGRAM_API_URL = 'https://api.telegram.org/bot' + self.API_TOKEN + '/getMe'
        self.SECRET_KEY = settings.SECRET_KEY

        ### database ###
        
        self.database = DataBase(self.flask, 'database.db')

        ### parser for searching ###

        self.parser = Parser(dictionary.types | dictionary.names)

        ### 2gis api key ###

        self.TWOGIS_API_KEY = 'ab7b70c9-9132-468f-8b4c-87177a2418cf'

        ### flask pages callback functions ###

        # home flask function
        @self.flask.route('/')
        def home():
            # user info setup
            session["last_location_search"] = ""
            session["user"] = pickle.dumps(self.database.get('User', 'name', 'Test')[0])

            return render_template('login.html')

        # User page selector flask callback function
        @self.flask.route('/selector', methods=['GET'])
        def selector():
            return render_template('selector.html')

        # Route to get all users
        @self.flask.route('/users', methods=['GET'])
        def get_users():
            self.database.start()
            if User.query.count() == 0:
                partner1 = Partner(type='кафе', name='буше', org_id=5348561428447988,
                                   image_url="https://avatars.mds.yandex.net/get-altay/4377463/2a00000182500a731822c9b8459bae41d2ab/L_height",
                                   logo_url="https://s.rbk.ru/v1_companies_s3/media/trademarks/1a677d0a-a614-4a7f-b77b-66d9d32a9d01.jpg")
                partner2 = Partner(type='кафе', name='бургер-кинг', org_id=5348561428715954, 
                                   image_url="https://avatars.mds.yandex.net/get-altay/12813249/2a00000190efe540d510a58448956515d257/L_height",
                                   logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Burger_King_2020.svg/1879px-Burger_King_2020.svg.png")
                partner3 = Partner(type='магазин', name='буквоед', org_id=5348561428522889, 
                                   image_url='https://tk-pik.ru/upload/iblock/443/jwv04az84jls77l83kntpr2t4ro6zivi.jpg',
                                   logo_url='https://habrastorage.org/getpro/moikrug/uploads/company/100/006/555/7/logo/medium_d5e9f242395f4a3c48abd90527fa74ce.png')
                partner4 = Partner(type='аптека', name='невис', org_id=5348561428415840, 
                                   image_url='https://s.zagranitsa.com/images/guides/20578/original/248baffaea928f45c0bb102e02dc1336.jpg?1441900197',
                                   logo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFV7M59LEzxJmcjxxImrEbJPrNCrs-zSqvlg&s')
                partner5 = Partner(type='заправка', name='лукойл', org_id=5348561428486914, 
                                   image_url='https://iy.kommersant.ru/Issues.photo/Partners_Docs/2024/11/22/KMO_111307_61034_1_t222_145337.jpg',
                                   logo_url='https://cdn.forbes.ru/forbes-static/new/2021/11/Company-619d3288c340a-619d3288e8cde.png')
                partner6 = Partner(type='заправка', name='роснефть', org_id=5348561428520571, 
                                   image_url='https://hdlt.ru/assets/template/upload/indoor/azs_rosneft/IMG_4538.jpg',
                                   logo_url='https://foni.papik.pro/uploads/posts/2024-10/foni-papik-pro-8xho-p-kartinki-rosneft-na-prozrachnom-fone-17.png')
                partner7 = Partner(type='аптека', name='лека-фарм', org_id=5348561428417650, 
                                   image_url='https://avatars.mds.yandex.net/get-altay/5751673/2a0000017cc56582485d205b1bcc888295b3/L_height',
                                   logo_url='https://lekafarm.ru/template/images/logo.png')
                partner8 = Partner(type='магазин', name='перекрёсток', org_id=5348561428466924, 
                                   image_url='https://static.tildacdn.com/tild6131-6632-4564-a262-633433623838/1a8a32_ca8931ce69e94.jpg',
                                   logo_url='https://www.perekrestok.ru/logo.png')
                self.database.add(partner1)
                self.database.add(partner2)
                self.database.add(partner3)
                self.database.add(partner4)
                self.database.add(partner5)
                self.database.add(partner6)
                self.database.add(partner7)
                self.database.add(partner8)

                user1 = User(type='Support', name='Test', email='test@gmail.com', telegram='@test', birthday=datetime.date(2008, 1, 25))
                self.database.add(user1)

                support1 = Support(user_id=user1.id)
                self.database.add(support1)

                chat1 = SupportChat(messages=json.dumps([{'sender': 'user', 'message': 'Hello, I need help!'}, {'sender': 'support', 'message': 'SHUT YA BITCH ASS UP!!!!!!'}]), user=user1.id, support=0)
                self.database.add(chat1)

            partners = Partner.query.all()
            return jsonify([{'type': partner.type, 'name': partner.name, 'image_url': partner.image_url, 'logo_url': partner.logo_url, 'org_id': partner.org_id} for partner in partners])

        # main page callback function
        @self.flask.route('/home', methods=['GET'])
        def main():
            return render_template('user/home.html',
                                   user=pickle.loads(self.get_var("user")),
                                   top_discount_partners=self.database.get_sort('Partner', 'name', 10))

        # map page flask callback function
        @self.flask.route('/map_empty', methods=['GET'])
        def map_empty():
            return render_template('user/map.html', locations=[])

        ### flask inner callback functions ###

        # user location saving function
        @self.flask.route('/save_user_location/<float:lat>/<float:lon>', methods=['POST'])
        def save_user_location(lat, lon):
            session["lat"] = lat
            session["lon"] = lon
            return '', 204

        # flask location search bar callback function
        @self.flask.route('/map', methods=['POST'])
        def map():
            user_input = request.form['location_search_bar']
            session["last_location_search"] = user_input

            if user_input != '':
                locations = search_closest_locations(session['lat'], session['lon'], user_input)
                return render_template('user/map.html', locations=locations)
            return redirect(url_for('map_empty'))

        # flask location search bar callback function
        @self.flask.route('/filtered_location_search', methods=['GET'])
        def filtered_location_search():
            type = request.form.get('filter_button')
            session["last_location_search"] = type
            locations = search_closest_locations(session['lat'], session['lon'], type)
            return render_template('user/map.html', locations=locations)

        # flask support callback function
        @self.flask.route('/support', methods=['GET'])
        def support():
            user_info = pickle.loads(self.get_var("user"))
            
            chat = self.database.get('SupportChat', 'user', user_info.id)
            if len(chat) == 0:
                chat = SupportChat(messages='[]', user=user_info.id, support=0)
                self.database.add(chat)
                return render_template('user/support.html', user=user_info, user_id=user_info.id, messages='[]')
    
            chat = chat[0]
            return render_template('user/support.html', user=user_info, user_id=user_info.id, messages=json.loads(chat.messages))
        
        # flask socket io handling function
        @self.socketio.on('message')
        def handle_message(msg):
            print('Message received: ' + json.loads(msg)['text'])
            print('Sender:           ' + str(json.loads(msg)['sender']))
            chat = self.database.get('SupportChat', 'user', json.loads(msg)['sender'])[0]
            new_messages = json.loads(chat.messages)
            new_messages.append({'sender': 'user', 'message': json.loads(msg)['text']})
            chat.messages = json.dumps(new_messages)
            self.database.update(chat)
            emit('message', msg, broadcast=True)

        # flask user profile callback function
        @self.flask.route('/profile', methods=['GET'])
        def profile():
            return render_template('user/profile.html', user=pickle.loads(self.get_var("user")))


        ### help functions ###

        # closest locations based on query searching function
        def search_closest_locations(lat, lon, query):
            url = f"https://catalog.api.2gis.com/3.0/items"
            locations = []

            text = self.parser.parse(query)
            partners = []

            if text in dictionary.types:
                partners = self.database.get('Partner', 'type', text)
            elif text in dictionary.names:
                partners = self.database.get('Partner', 'name', text)

            for partner in partners:
                params = {
                    'key': self.TWOGIS_API_KEY,
                    'point': f"{lon},{lat}",
                    # 'page_size': 30,
                    'radius': 2000,  # радиус поиска в метрах
                    # 'type': 'adm_div.city',
                    'org_id': partner.org_id,
                    # 'q': query,
                    'fields': 'items.point,items.org',
                    'sort': 'distance',
                }
                response = requests.get(url, params=params)

                if response.status_code != 200:
                    print('2gis error')
                    return jsonify({"error": "Failed to fetch data from 2GIS"}), 500

                data = response.json()

                if 'result' in data:
                    for item in data['result']['items']:
                        locations.append({
                            'name': partner.name,
                            # 'address': item['address_name'],
                            'point': item['point'],
                            'img': partner.image_url,
                            'logo': partner.logo_url
                        })

            return locations

# application instance
app = App()

# application entry point for local debug
if __name__ == '__main__':
    app.run()