# imports
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import requests
import pickle
import json
import datetime
import settings

# database
from database import *

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
        self.socketio.run(self.flask, debug=True)

    # class initialization function
    def __init__(self):
        ### local class variables ###

        # flask
        self.flask = Flask(__name__)
        self.flask.secret_key = 'GiantAlienDildo'
        self.socketio = SocketIO(self.flask)

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

        ### flask pages callback functions not role based ###

        # home flask function
        @self.flask.route('/')
        def login():
            # user info setup
            session['last_location_search'] = ''
            session['user'] = pickle.dumps(self.database.get_one('User', 'telegram', '@manager')) # telegram id should be obtained via TelegramAPI
            session['prev_page'] = 'home'

            return render_template('login.html')

        # User page selector flask callback function
        @self.flask.route('/selector', methods=['GET'])
        def selector():
            return render_template('selector.html',
                                   user=pickle.loads(session['user']))


        ### database recreation flask callback function ###

        # Route to get all users
        @self.flask.route('/users', methods=['GET'])
        def get_users():
            self.database.start()
            if User.query.count() == 0:
                partner1 = Partner(type='кафе', name='буше', org_id=5348561428447988,
                                   image_urls=json.dumps([
                                    'https://avatars.mds.yandex.net/get-altay/4377463/2a00000182500a731822c9b8459bae41d2ab/L_height',
                                    'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0a/42/bb/5f/caption.jpg?w=900&h=500&s=1'
                                    ]),
                                   logo_url='https://s.rbk.ru/v1_companies_s3/media/trademarks/1a677d0a-a614-4a7f-b77b-66d9d32a9d01.jpg',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner2 = Partner(type='кафе', name='бургер-кинг', org_id=5348561428715954, 
                                   image_urls=json.dumps(['https://avatars.mds.yandex.net/get-altay/12813249/2a00000190efe540d510a58448956515d257/L_height']),
                                   logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Burger_King_2020.svg/1879px-Burger_King_2020.svg.png',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner3 = Partner(type='магазин', name='буквоед', org_id=5348561428522889, 
                                   image_urls=json.dumps(['https://tk-pik.ru/upload/iblock/443/jwv04az84jls77l83kntpr2t4ro6zivi.jpg']),
                                   logo_url='https://habrastorage.org/getpro/moikrug/uploads/company/100/006/555/7/logo/medium_d5e9f242395f4a3c48abd90527fa74ce.png',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner4 = Partner(type='аптека', name='невис', org_id=5348561428415840, 
                                   image_urls=json.dumps(['https://s.zagranitsa.com/images/guides/20578/original/248baffaea928f45c0bb102e02dc1336.jpg?1441900197']),
                                   logo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFV7M59LEzxJmcjxxImrEbJPrNCrs-zSqvlg&s',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner5 = Partner(type='заправка', name='лукойл', org_id=5348561428486914, 
                                   image_urls=json.dumps(['https://iy.kommersant.ru/Issues.photo/Partners_Docs/2024/11/22/KMO_111307_61034_1_t222_145337.jpg']),
                                   logo_url='https://cdn.forbes.ru/forbes-static/new/2021/11/Company-619d3288c340a-619d3288e8cde.png',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner6 = Partner(type='заправка', name='роснефть', org_id=5348561428520571, 
                                   image_urls=json.dumps(['https://hdlt.ru/assets/template/upload/indoor/azs_rosneft/IMG_4538.jpg']),
                                   logo_url='https://foni.papik.pro/uploads/posts/2024-10/foni-papik-pro-8xho-p-kartinki-rosneft-na-prozrachnom-fone-17.png',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner7 = Partner(type='аптека', name='лека-фарм', org_id=5348561428417650, 
                                   image_urls=json.dumps(['https://avatars.mds.yandex.net/get-altay/5751673/2a0000017cc56582485d205b1bcc888295b3/L_height']),
                                   logo_url='https://lekafarm.ru/template/images/logo.png',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner8 = Partner(type='магазин', name='перекрёсток', org_id=5348561428466924, 
                                   image_urls=json.dumps(['https://static.tildacdn.com/tild6131-6632-4564-a262-633433623838/1a8a32_ca8931ce69e94.jpg']),
                                   logo_url='https://www.perekrestok.ru/logo.png',
                                   sales=json.dumps([
                                    Sale(90, 'Free cum for anybody!'),
                                    Sale(40, 'Not that free cum'),
                                   ], cls=SaleEncoder),
                                   rating=4.4,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                self.database.add(partner1)
                self.database.add(partner2)
                self.database.add(partner3)
                self.database.add(partner4)
                self.database.add(partner5)
                self.database.add(partner6)
                self.database.add(partner7)
                self.database.add(partner8)

                user_superadmin = User(type='Superadmin', name='Superadminovich', email='superadmin@gmail.com', telegram='@superadmin', birthday=datetime.date(2008, 1, 25), last_partners="[]")
                user_admin = User(type='Admin', name='Adminovich', email='admin@gmail.com', telegram='@admin', birthday=datetime.date(2008, 4, 16), last_partners="[]")
                user_support = User(type='Support', name='Supportovich', email='support@gmail.com', telegram='@support', birthday=datetime.date(2008, 3, 29), last_partners="[]")
                user_director = User(type='Director', name='Directorovich', email='director@gmail.com', telegram='@director', birthday=datetime.date(2008, 2, 1), last_partners="[]")
                user_manager = User(type='Manager', name='Managerorovich', email='manager@gmail.com', telegram='@manager', birthday=datetime.date(1945, 5, 9), last_partners="[]")
                user_user = User(type='User', name='Userovich', email='user@gmail.com', telegram='@user', birthday=datetime.date(2001, 9, 11), last_partners="[]")
                self.database.add(user_superadmin)
                self.database.add(user_admin)
                self.database.add(user_support)
                self.database.add(user_director)
                self.database.add(user_manager)
                self.database.add(user_user)

                director1 = Director(user_id=user_director.id, partner_id=partner1.id)
                self.database.add(director1)
                manager1 = Manager(user_id=user_manager.id, partner_id=partner2.id)
                self.database.add(manager1)
                support1 = Support(user_id=user_support.id)
                self.database.add(support1)

                chat1 = SupportChat(messages=json.dumps([{'sender': 'user', 'message': 'Hello, I need help!'}, {'sender': 'support', 'message': 'SHUT YA BITCH ASS UP!!!!!!'}]), user=user_support.id, support=0)
                self.database.add(chat1)

            partners = Partner.query.all()
            return jsonify([{'type': partner.type, 'name': partner.name, 'image_url': partner.image_urls, 'logo_url': partner.logo_url, 'org_id': partner.org_id, 'sales': partner.sales} for partner in partners])


        ### user flask callback functions ###

        # flask location search bar callback function
        @self.flask.route('/user/map', methods=['POST', 'GET'])
        def map():
            session['prev_page'] = 'map'

            user_input = session['last_location_search']
            if request.method == 'POST':
                if 'search_bar' in request.form:
                    user_input = request.form['search_bar']
                else:
                    user_input = request.form.get('filter_button')
                session['last_location_search'] = user_input

            if user_input != '':
                locations = search_closest_locations(session['lat'], session['lon'], user_input)
                return render_template('user/map.html', locations=locations)
            return render_template('user/map.html', locations=[])


        # flask support callback function
        @self.flask.route('/user/support', methods=['GET'])
        def support():
            user_info = pickle.loads(session['user'])
            
            chat = self.database.get('SupportChat', 'user', user_info.id)
            if len(chat) == 0:
                chat = SupportChat(messages='[]', user=user_info.id, support=0)
                self.database.add(chat)
                return render_template('user/support.html', user=user_info, user_id=user_info.id, messages='[]')
    
            chat = chat[0]
            return render_template('user/support.html', user=user_info, user_id=user_info.id, messages=json.loads(chat.messages))

        # main page callback function
        @self.flask.route('/user/home', methods=['GET'])
        def main():
            session['prev_page'] = 'home'

            user = pickle.loads(session['user'])
            last_partners = json.loads(user.last_partners)
            size = len(last_partners)
            for i in range(0, size):
                last_partners[i] = self.database.get_one('Partner', 'id', last_partners[i])
            return render_template('user/home.html',
                                   user=user,
                                   last_partners=last_partners,
                                   top_discount_partners=self.database.get_sort('Partner', 'best_sale_amount', 10),
                                   top_rating_partners=self.database.get_sort('Partner', 'rating', 10))

        # partners searching flask callback function
        @self.flask.route('/user/partners_list', methods=['POST', 'GET'])
        def partners_list():
            session['prev_page'] = 'partners_list'

            user_input = session['last_location_search']
            if request.method == 'POST':
                user_input = request.form['search_bar']
                session['last_location_search'] = user_input

            text = self.parser.parse(user_input)
            partners = []

            if text in dictionary.types:
                partners = self.database.get('Partner', 'type', text)
            elif text in dictionary.names:
                partners = self.database.get('Partner', 'name', text)
                
            return render_template('user/partners_list.html', partners=partners)

        # single partner info flask callback function
        @self.flask.route('/user/partner', methods=['POST'])
        def partner():
            partner = self.database.get('Partner', 'id', request.form['partner_button'])[0]
            user = pickle.loads(session['user'])

            last_partners = json.loads(user.last_partners)
            last_partners = [partner.id] + [i for i in last_partners if i != partner.id]
            user.last_partners = json.dumps(last_partners)
            self.database.update(user)

            session['user'] = pickle.dumps(user)
            return render_template('user/partner.html', partner=partner)

        # getting back from partner page flask callback function
        @self.flask.route('/user/back', methods=['GET'])
        def partner_back():
            return redirect(url_for(session['prev_page']), 301)

        # flask user profile callback function
        @self.flask.route('/user/profile', methods=['GET'])
        def profile():
            return render_template('user/profile.html', user=pickle.loads(session['user']))


        ### flask inner callback functions ###

        # user location saving function
        @self.flask.route('/save_user_location/<float:lat>/<float:lon>', methods=['POST'])
        def save_user_location(lat, lon):
            session['lat'] = lat
            session['lon'] = lon
            return '', 204
        
        # flask socket io handling function
        @self.socketio.on('message')
        def handle_message(msg):
            print('Message received: ' + json.loads(msg)['text'])
            print('Sender:           ' + str(json.loads(msg)['sender']))
            chat = self.database.get_one('SupportChat', 'user', json.loads(msg)['sender'])
            new_messages = json.loads(chat.messages)
            new_messages.append({'sender': 'user', 'message': json.loads(msg)['text']})
            chat.messages = json.dumps(new_messages)
            self.database.update(chat)
            emit('message', msg, broadcast=True)

        
        ### admin role flask callback functions ### 

        # roles management flask callback function
        @self.flask.route('/admin/roles', methods=['GET'])
        def admin_roles():
            if pickle.loads(session['user']).type in ['Superadmin', 'Admin', 'Director', 'Manager']:       
                return render_template('admin/roles.html',
                                        user=pickle.loads(session['user']),
                                        users=self.database.get_sort('User', 'name', 100))
            else:
                return render_template('error.html')
                
        
        # parter editing page flask callback function
        @self.flask.route('/admin/partner', methods=['GET'])
        def admin_partner():
            user = pickle.loads(session['user'])
            if user.type in ['Director', 'Manager']:
                partner_admin = self.database.get_one(user.type, 'user_id', user.id)
                print(partner_admin)
                return render_template('admin/partner.html',
                                        user=user,
                                        partner=self.database.get_one('Partner', 'id', partner_admin.partner_id))
            else:
                return render_template('error.html')
        
        # reviews flask callback function
        @self.flask.route('/admin/reviews', methods=['GET'])
        def admin_reviews():
            if pickle.loads(session['user']).type in ['Director', 'Manager']:       
                return render_template('admin/reviews.html',
                                        user=pickle.loads(session['user']))
            else:
                return render_template('error.html')
        
        # support flask callback function
        @self.flask.route('/admin/support', methods=['GET'])
        def admin_support():
            if pickle.loads(session['user']).type in ['Support']:       
                return render_template('admin/support.html',
                                        user=pickle.loads(session['user']))
            else:
                return render_template('error.html')

        ### help functions ###

        # closest locations based on query searching function
        def search_closest_locations(lat, lon, query):
            url = f'https://catalog.api.2gis.com/3.0/items'
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
                    'point': f'{lon},{lat}',
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
                    return jsonify({'error': 'Failed to fetch data from 2GIS'}), 500

                data = response.json()

                if 'result' in data:
                    for item in data['result']['items']:
                        locations.append({
                            'name': partner.name,
                            # 'address': item['address_name'],
                            'point': item['point'],
                            'logo': partner.logo_url,
                            'partner_id': partner.id
                        })

            return locations

# application instance
app = App()

# application entry point for local debug
if __name__ == '__main__':
    app.run()