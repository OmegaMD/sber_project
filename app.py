#! /usr/bin/env python
# -*- coding: utf-8 -*-


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
        #self.socketio.run(self.flask, debug=False, host = '185.139.69.44', port = 8000)
        #self.socketio.run(self.flask, allow_unsafe_werkzeug=True, debug = True)
        
        #eventlet.monkey_patch()  # Add eventlet monkey patching
        self.socketio.run(self.flask, debug=True)

    # class initialization function
    def __init__(self):
        ### local class variables ###

        # flask
        self.flask = Flask(__name__)
        self.flask.secret_key = settings.FLASK_KEY
        self.socketio = SocketIO(self.flask)

        # API token and secret for Telegram login
        self.API_TOKEN = settings.API_TOKEN       

        # URL для проверки авторизации
        self.SECRET_KEY = settings.SECRET_KEY

        # support system
        self.next_support = 0

        ### database ###

        self.database = DataBase(self.flask, 'database.db')

        ### parser for searching ###

        self.parser = Parser(dictionary.types | dictionary.names)


        ### flask pages callback functions not role based ###

        # home flask function
        @self.flask.route('/')
        def login():
            # user info setup
            session['last_location_search'] = ''
            # session['user_id'] = self.database.get_one('User', 'telegram', '@director').id # telegram id should be obtained via TelegramAPI
            session['prev_page'] = 'home'
            session['saved_loc'] = 'false'

            return render_template('login.html')

        # User page selector flask callback function
        @self.flask.route('/selector', methods=['GET'])
        def selector():
            username = request.args.get('username', default = '*', type = str)
            users = self.database.get('User', 'telegram', username)
            uesr = None
            if len(users) == 0:
                first_name = request.args.get('first_name', default = '*', type = str)

                user = User(type='User', name=first_name, email='пока пусто', telegram=username, birthday=datetime.date(1841, 11, 12), last_partners='[]')
                self.database.add(user)
            else:
                user = users[0]
            
            # user = self.database.get_one('User', 'telegram', 'STEmug')
            session['user_id'] = user.id
            return render_template('selector.html', user=user)


        ### database recreation flask callback function ###

        # Route to get all users
        @self.flask.route('/users', methods=['GET'])
        def get_users():
            self.database.start()
            if User.query.count() == 0:
                partner1 = Partner(type='кафе', name='буше', org_id=5348561428447988,
                                   image_urls=json.dumps([
                                    'https://avatars.mds.yandex.net/get-altay/4377463/2a00000182500a731822c9b8459bae41d2ab/L_height',
                                    'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0a/42/bb/5f/caption.jpg?w=900&h=500&s=1',
                                    'https://avatars.mds.yandex.net/i?id=a9956feb4708783ec55290d5f77e2ead7a4fd006-3675323-images-thumbs&n=13',
                                    'https://avatars.mds.yandex.net/i?id=d0f94acab7dbb464c470813b4de03b6a27f8d3c6-4570467-images-thumbs&n=13',
                                    'https://avatars.mds.yandex.net/i?id=025ba15ee4a9af9a0a38ddf0773a620596174f54-5241497-images-thumbs&n=13'
                                    ]),
                                   logo_url='https://s.rbk.ru/v1_companies_s3/media/trademarks/1a677d0a-a614-4a7f-b77b-66d9d32a9d01.jpg',
                                   sales=json.dumps([
                                    Sale(15, 'на всё для тех, кто скажет пароль: «Я люблю Буше, как француз любят багеты»'),
                                    Sale(50, 'на каждый второй круассан с 8:00 до 10:00 в будни'),
                                   ], cls=SaleEncoder),
                                   rating=3.6,
                                   info='«Быть живым в каждый момент времени» — это парадигма буше, которая лежит в основе всего, что мы делаем, аж с 10 февраля 1999 года, когда открылось первое буше на улице Разъезжая дом 13.',
                                   best_sale_amount=90)
                partner2 = Partner(type='кафе', name='бургер-кинг', org_id=5348561428715954, 
                                   image_urls=json.dumps([
                                       'https://avatars.mds.yandex.net/get-altay/12813249/2a00000190efe540d510a58448956515d257/L_height',
                                       'https://avatars.mds.yandex.net/i?id=b59eab9f47757472a590b6e50fe98042259972af-5231880-images-thumbs&n=13',
                                       'https://yandex-images.clstorage.net/ne5di1170/416a96KDj/AOYtD49-94usO0sXFMqfsYjt2P1I6kQwSAr64rvyhgapdTQ1v_TlalBQrrMJ1uyq8y2Se7t_Qy8F-wcTukWJxk3_bVq-a-_i_X5PekTqk6WAmK3xDJssITxj85PDpr46jWhg3AoQZfvtsSIbnDpFl78FlmqTHwIn8R4CfuMliYuw7h3rY77aozT_gmc0LrO52FQITRwDkAGQuvOH-9_Ka6SFoMiSVKmn2bn6nwgW-buLjUK6-nsaxxFfPmLHoYmPWHqFxwPScnsk_wKraPIv7biQWOl89_wR9KYPo-t_SreYfYQcxgDBw_mJ7ndMrskznx3aTnYv_lfdy8p-vyG9a5x-GfsjDp4LyPtuH3gWl8FEWNTVAKtEhWyqWyO_q97LoHngbKKgeRuNZaKnvP7tawdt7j5qC_Lvxd8qWsO5JX-Ybo1vy4Zmv4ALnjPI-jv5JAgI3eST1H0wkrcv4zN2l0ipDJTu_NWTMcHy78Q6wecb2cYaYvMqNyErSpbjvYWbvKI146t6YgssG94j1AZ7GbRoqGE4GxhBdM7vD6tXtq_kYTycPoTNm0mBptfUPiXPby3K5ma_ItNNJ77KW13RR-Rq6Q-zYqoTwBvKExD6w0HUEOTlPH9MoaRm58efr7KLREU8nGpAWccxEUoXBKZNt2etVq5qhy5_6cemLi9FMRtgJoHzq46Ob7z3nvd8epM9LJxwnWS_sK1khi_Dl796x0D1vJzCULEzob0CM9iKxVuPWVL62seam607rlZPqYWHVLbxzyu6mqNMpwKfbHIrQQQAQEE8U6AFEB4LQ3NzHhNIlfSoVlR5T6Epen9EivE3G6FGNkoTKpuhI57C-zl1VwwKJVPPCl6LPJ_mB6jeA2EEpOTB4L-ouawix_9r_96zyGXkvJ4I6XuJ7TrvrEq155PhHtouF-4byV_GZi9Rhedcnk1_gwKaf7QfRotIkvcZlLwEBfiLJEkgSq8nH2uQ',
                                       'https://avatars.mds.yandex.net/i?id=2fa0ace9051b7e5f8b30eafe867aa8b2449f72af-12884996-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=51bc093253c7d569e224b384f39bde4cd6b3ef2a-4422933-images-thumbs&n=13'
                                       ]),
                                   logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Burger_King_2020.svg/1879px-Burger_King_2020.svg.png',
                                   sales=json.dumps([
                                    Sale(25, 'на любую позицию, если приведете друга'),
                                    Sale(40, 'на завтраки по утрам'),
                                   ], cls=SaleEncoder),
                                   rating=1.6,
                                   info='мировой фастфуд-гигант, где готовят огромные сочные бургеры на огне, хрустящую картошку и легендарные Whopperы. У нас можно собрать бургер мечты, обмакнуть наггетсы в десять видов соуса и запить всё ледяной Coca-Cola. Быстро, вкусно и без лишних церемоний!',
                                   best_sale_amount=90)
                partner3 = Partner(type='магазин', name='буквоед', org_id=5348561428522889, 
                                   image_urls=json.dumps([
                                       'https://tk-pik.ru/upload/iblock/443/jwv04az84jls77l83kntpr2t4ro6zivi.jpg',
                                       'https://avatars.mds.yandex.net/i?id=b60c0f9336c9a8cffb5275906c03677557f70bf5-5332940-images-thumbs&n=13',
                                       'https://yandex-images.clstorage.net/ne5di1170/416a96KDj/AOYtD49-94usO0sXFMqfsYjt2P1I6kQwSAr64_qzy16oOTVtupD4IxUEs-pB35y2-y2DPuY3RxJItmJDqlzZ0lSmLAq-Z-vSzU5DakTqk6WAmK3xDJssITxj85PDpr46jWhg3AoQZfvtsSIbnDpFl78FlmqTHwIn8R4CfuMliYuw7h3rY77aozT_gmc0LrO52FQITRwDkAGQuvOH-9_Ka6SFoMiSVKmn2bn6nwgW-buLjUK6-nsaxxFfPmLHoYmPWHqFxwPScnsk_wKraPIv7biQWOl89_wR9KYPo-t_SreYfYQcxgDBw_mJ7ndMrskznx3aTnYv_lfdy8p-vyG9a5x-GfsjDp4LyPtuH3gWl8FEWNTVAKtEhWyqWyO_q97LoHngbKKgeRuNZaKnvP7tawdt7j5qC_Lvxd8qWsO5JX-Ybo1vy4Zmv4ALnjPI-jv5JAgI3eST1H0wkrcv4zN2l0ipDJTu_NWTMcHy78Q6wecb2cYaYvMqNyErSpbjvYWbvKI146t6YgssG94j1AZ7GbRoqGE4GxhBdM7vD6tXtq_kYTycPoTNm0mBptfUPiXPby3K5ma_ItNNJ77KW13RR-Rq6Q-zYqoTwBvKExD6w0HUEOTlPH9MoaRm58efr7KLREU8nGpAWccxEUoXBKZNt2etVq5qhy5_6cemLi9FMRtgJoHzq46Ob7z3nvd8epM9LJxwnWS_sK1khi_Dl796x0D1vJzCULEzob0CM9iKxVuPWVL62seam607rlZPqYWHVLbxzyu6mqNMpwKfbHIrQQQAQEE8U6AFEB4LQ3NzHhNIlfSoVlR5T6Epen9EivE3G6FGNkoTKpuhI57C-zl1VwwKJVPPCl6LPJ_mB6jeA2EEpOTB4L-ouawix_9r_96zyGXkvJ4I6XuJ7TrvrEq155PhHtouF-4byV_GZi9Rhedcnk1_gwKaf7QfRotIkvcZlLwEBfiLJEkgSq8nH2uQ',
                                       'https://avatars.mds.yandex.net/i?id=006e1ed3f3d2131df7a5dc7a43654ee9d1ba8a98-7013580-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=fbece12e5de01159bc02ab70b3b51971c787fcee-5597167-images-thumbs&n=13'
                                       ]),
                                   logo_url='https://yandex-images.clstorage.net/ne5di1170/416a96KDj/AOYtD49-94usO0sXFMqfsYjt2P1I6kQwSAr64_qzy16oOTVtupD4IxUEs-pB35y2-y2DPuY3RxJItmJDqlzZ0lSmLAq-Z-vSzU5DakTqk6WAmK3xDJssITxj85PDpr46jWhg3AoQZfvtsSIbnDpFl78FlmqTHwIn8R4CfuMliYuw7h3rY77aozT_gmc0LrO52FQITRwDkAGQuvOH-9_Ka6SFoMiSVKmn2bn6nwgW-buLjUK6-nsaxxFfPmLHoYmPWHqFxwPScnsk_wKraPIv7biQWOl89_wR9KYPo-t_SreYfYQcxgDBw_mJ7ndMrskznx3aTnYv_lfdy8p-vyG9a5x-GfsjDp4LyPtuH3gWl8FEWNTVAKtEhWyqWyO_q97LoHngbKKgeRuNZaKnvP7tawdt7j5qC_Lvxd8qWsO5JX-Ybo1vy4Zmv4ALnjPI-jv5JAgI3eST1H0wkrcv4zN2l0ipDJTu_NWTMcHy78Q6wecb2cYaYvMqNyErSpbjvYWbvKI146t6YgssG94j1AZ7GbRoqGE4GxhBdM7vD6tXtq_kYTycPoTNm0mBptfUPiXPby3K5ma_ItNNJ77KW13RR-Rq6Q-zYqoTwBvKExD6w0HUEOTlPH9MoaRm58efr7KLREU8nGpAWccxEUoXBKZNt2etVq5qhy5_6cemLi9FMRtgJoHzq46Ob7z3nvd8epM9LJxwnWS_sK1khi_Dl796x0D1vJzCULEzob0CM9iKxVuPWVL62seam607rlZPqYWHVLbxzyu6mqNMpwKfbHIrQQQAQEE8U6AFEB4LQ3NzHhNIlfSoVlR5T6Epen9EivE3G6FGNkoTKpuhI57C-zl1VwwKJVPPCl6LPJ_mB6jeA2EEpOTB4L-ouawix_9r_96zyGXkvJ4I6XuJ7TrvrEq155PhHtouF-4byV_GZi9Rhedcnk1_gwKaf7QfRotIkvcZlLwEBfiLJEkgSq8nH2uQ',
                                   sales=json.dumps([
                                    Sale(70, 'на третью книгу при покупке в интернет магазине'),
                                    Sale(50, 'на всё в день рождения'),
                                   ], cls=SaleEncoder),
                                   rating=5.0,
                                   info='это не просто книжный, а культурное пространство с атмосферой интеллектуального комфорта. Мы не просто продаем книги — мы создаем место, где рождается любовь к чтению.',
                                   best_sale_amount=90)
                partner4 = Partner(type='аптека', name='невис', org_id=5348561428415840, 
                                   image_urls=json.dumps([
                                       'https://s.zagranitsa.com/images/guides/20578/original/248baffaea928f45c0bb102e02dc1336.jpg?1441900197',
                                       'https://yandex-images.clstorage.net/ne5di1170/416a96KDj/AOYtD49-94usO0sXFMqfsYjt2P1I6kQwSAr64_q-shapdElBs8G4EnRcq9pdz7i3qmDPJ7tvXypAtk5PxlTUhk3zaD6_Eo63hD9LGyDu85WUwfjBaPoULEFrp2sLY1aLBJHkhGowWRcVNfqrYaa1p0fAhkbiA14nubM28huJ_c-oaq0Xz9auq9zz7qcwdk-1OBj41VCDYH1ohmd_kyea1zCZPAD-HOU7Ib0uewjCrUengbpaxodeI1Enrt575VUXuGot25MKMv-8N74DUIIjpVwEBPFAI-ChVH5Dq8dz8rMQqSjouqTVszUtto-ElknXaxVORr4HaseVIzLiWzm5Z1RuQW-D7orTQP8yPyzemzHECFBxFPd03Wx6J9uj00prZEVkOEr08eutXYL_mLJFb3MBrmLCn_LTkTOmdrOxQdMcnrFDMwIm6yCv7jfI5gvJmDC8fUhv3IGEqssj74_m49jhNHAyMN1nsemq25BKnbeX9c6u4ptSN7X_HvrTTUVnsI7xUy_-Zguwz06LFG7H9dxs5F0ACxy5KGL7Kz_3_uugoWBIIjQ5T8UdpieUBpVT-_k68lp7BuvtN8IWy1WNf1yO5WPrAt5T0LcCDxAKkxUMxOyVNPMYnYhG-ytrM2q32DGMiPKsUTfNnTpvmD6Z_18ZIhYuY-a3aXuq6tO5qQMgYrGHh4KOLyg7lndIym8ZzCQkkTzj0NGM9nsrwyOCQ0idxKwugNnbJWk-Oyh-LRsb5SpuTo9SK13r2tZTjb3P0DIt75eKNlMAp6arECZ_sbi8ABHYL7QFhJYzH1cnSj9ICbzgsoDtt7GRKve4qp0bF_0a-vofovsFVw5Ktz1556AKyXdTJh5zAAMCK8zKdw0EgMytwKN0pQRmIwufe9oLYM38cFpAqWc50XIb3K5Zm3-BQl4ud1JLVcNmZvs1vRMoimn7s2rqC5Ab4u_U_vv9iOikdbQ3OC18zkNTZ3Pg'
                                       ]),
                                   logo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFV7M59LEzxJmcjxxImrEbJPrNCrs-zSqvlg&s',
                                   sales=json.dumps([
                                    Sale(25, 'на все витамины при покупке от 2000₽'),
                                    Sale(100, 'на доставку рецептурных лекарств'),
                                   ], cls=SaleEncoder),
                                   rating=4.2,
                                   info='современная аптечная сеть с человеческим лицом. Мы предлагаем не просто лекарства, а комплексную заботу о здоровье. Наши принципы: профессионализм, доступные цены и душевное отношение к каждому покупателю.',
                                   best_sale_amount=90)
                partner5 = Partner(type='заправка', name='лукойл', org_id=5348561428486914, 
                                   image_urls=json.dumps([
                                       'https://iy.kommersant.ru/Issues.photo/Partners_Docs/2024/11/22/KMO_111307_61034_1_t222_145337.jpg',
                                       'https://avatars.mds.yandex.net/i?id=c7960058e819c3ddd25c38f303ffc8735147a506-4589186-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=0050980037dcd2435cc77b3c570fc987a3cbd5bc-12597979-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=10965b39f13d1f1cc99630964b3edf5f9235c41a-11030990-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=da53b6bbcfe49b61d65f01f5d23c7379df3a01e3-5222505-images-thumbs&n=13'
                                       ]),
                                   logo_url='https://cdn.forbes.ru/forbes-static/new/2021/11/Company-619d3288c340a-619d3288e8cde.png',
                                   sales=json.dumps([
                                    Sale(7, 'на АИ-95 с 20:00 до 6:00.'),
                                    Sale(12, 'на АИ-98 при оплате через мобильное приложение'),
                                   ], cls=SaleEncoder),
                                   rating=4.2,
                                   info='одна из крупнейших сетей автозаправочных станций в России, предлагающая: качественное топливо с улучшенными присадками, Современные АЗС с магазинами, кафе и чистыми зонами отдыха, Программы лояльности (бонусы, кешбэк, скидки на ТО), Экологичные решения: зарядки для электромобилей и био-топливо',
                                   best_sale_amount=90)
                partner6 = Partner(type='заправка', name='роснефть', org_id=5348561428520571, 
                                   image_urls=json.dumps([
                                       'https://hdlt.ru/assets/template/upload/indoor/azs_rosneft/IMG_4538.jpg',
                                       'https://avatars.mds.yandex.net/i?id=4a6225ba4a0f70043dd162e27a9fd3f43c2c1cbf-9181121-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=295c7af01818a067d4004924902cbe99cbc429c8-4350902-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=d7d789a4522873172936c44ac5f6a992229c1c86-9843251-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=45bc9194a562c72d8eeb794b2ccfa10f6ae12eb8-5257898-images-thumbs&n=13'
                                       ]),
                                   logo_url='https://foni.papik.pro/uploads/posts/2024-10/foni-papik-pro-8xho-p-kartinki-rosneft-na-prozrachnom-fone-17.png',
                                   sales=json.dumps([
                                    Sale(7, 'на АИ-95 с 20:00 до 6:00.'),
                                    Sale(12, 'на АИ-98 при оплате через мобильное приложение'),
                                   ], cls=SaleEncoder),
                                   rating=3.8,
                                   info='одна из крупнейших сетей автозаправочных станций в России, предлагающая качественное топливо, удобные сервисы и выгодные программы лояльности. На наших АЗС вы найдете не только заправку, но и магазины с кофе, снеками, автохимией, а также чистые туалеты и бесплатный Wi-Fi. Мы заботимся о вашем комфорте в пути!',
                                   best_sale_amount=90)
                partner7 = Partner(type='аптека', name='лека-фарм', org_id=5348561428417650, 
                                   image_urls=json.dumps([
                                       'https://avatars.mds.yandex.net/get-altay/5751673/2a0000017cc56582485d205b1bcc888295b3/L_height',
                                       'https://avatars.mds.yandex.net/i?id=bea98c570875f88d14f1461b9f1ac9f6c66bcb4e-5503430-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=21d191b97fb84d3f4adb7f060e74cd28fa4d29e8-3287375-images-thumbs&n=13'
                                       ]),
                                   logo_url='https://lekafarm.ru/template/images/logo.png',
                                   sales=json.dumps([
                                    Sale(15, 'на все витамины — только сегодня с 10:00 до 12:00!'),
                                   ], cls=SaleEncoder),
                                   rating=3,
                                   info='это современная аптечная сеть с широким ассортиментом лекарств, косметики, БАДов и медицинских товаров. У нас работают компетентные фармацевты, действуют выгодные акции, а в некоторых аптеках есть даже экспресс-доставка. Главное — ваше здоровье и удобство!',
                                   best_sale_amount=90)
                partner8 = Partner(type='магазин', name='перекрёсток', org_id=5348561428466924, 
                                   image_urls=json.dumps([
                                       'https://static.tildacdn.com/tild6131-6632-4564-a262-633433623838/1a8a32_ca8931ce69e94.jpg',
                                       'https://avatars.mds.yandex.net/i?id=bf4cf66446010279e4dd5b5f17cda38d87374be8-4034266-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=e1ae103df28a6e0adea3160831a9b0647b317486-5282144-images-thumbs&n=13',
                                       'https://avatars.mds.yandex.net/i?id=2f33cff99107187458ea5403ff6953888340abf5-13197814-images-thumbs&n=13'
                                       ]),
                                   logo_url='https://www.perekrestok.ru/logo.png',
                                   sales=json.dumps([
                                    Sale(50, 'На всё из "Уголка сладкоежки": Торты, пирожные, шоколад и мармелад — вдвое дешевле! Успейте до конца недели, потому что такие сладости разлетаются, как горячие пирожки'),
                                    Sale(78, 'На готовую курочку после 21:00: Запечённая, гриль или в панировке — почти даром! Покупайте вкусный ужин со скидкой, пока магазин не закрылся. Идеально для полуночников и тех, кто забыл про ужин.'),
                                    Sale(30, 'На ВСЮ фермерскую продукцию: Свежие овощи, яйца, молоко и сыры от местных производителей — дешевле только на грядке! Только три дня — запасайтесь витаминами выгодно.'),
                                   ], cls=SaleEncoder),
                                   rating=3.6,
                                   info='«Перекрёсток» — это сеть современных продуктовых магазинов, где каждый найдёт свежие продукты, качественные товары повседневного спроса и приятные цены. У нас широкий ассортимент: от фермерских овощей и фруктов до готовых блюд, выпечки и деликатесов. Мы заботимся о вашем удобстве — в «Перекрёстке» всегда чисто, уютно и есть всё для быстрых и вкусных покупок.',
                                   best_sale_amount=90)
                self.database.add(partner1)
                self.database.add(partner2)
                self.database.add(partner3)
                self.database.add(partner4)
                self.database.add(partner5)
                self.database.add(partner6)
                self.database.add(partner7)
                self.database.add(partner8)

                user_superadmin = User(type='Superadmin', name='Максим', email='пока нету', telegram='OmegaMD', birthday=datetime.date(2008, 4, 16), last_partners='[]')
                # user_admin = User(type='Admin', name='Adminovich', email='admin@gmail.com', telegram='@admin', birthday=datetime.date(2008, 4, 16), last_partners='[]')
                # user_support = User(type='Support', name='Савва', email='savvapos2008@gmail.com', telegram='STEmug', birthday=datetime.date(2008, 1, 25), last_partners='[]')
                user_support1 = User(type='Support', name='Кирилл', email='пока нету', telegram='kirsdkv', birthday=datetime.date(2008, 3, 29), last_partners='[]')
                # user_director = User(type='Director', name='Directorovich', email='director@gmail.com', telegram='@director', birthday=datetime.date(2008, 2, 1), last_partners='[]')
                # user_manager = User(type='Manager', name='Managerorovich', email='manager@gmail.com', telegram='@manager', birthday=datetime.date(1945, 5, 9), last_partners='[]')
                # user_user = User(type='User', name='Userovich', email='user@gmail.com', telegram='@user', birthday=datetime.date(2001, 9, 11), last_partners='[]')
                self.database.add(user_superadmin)
                # self.database.add(user_admin)
                # self.database.add(user_support)
                self.database.add(user_support1)
                # self.database.add(user_director)
                # self.database.add(user_manager)
                # self.database.add(user_user)

                #director1 = Director(user_id=user_director.id, partner_id=partner1.id)
                #self.database.add(director1)
                # manager1 = Manager(user_id=user_manager.id, partner_id=partner2.id)
                # self.database.add(manager1)
                # support1 = Support(user_id=user_support.id)
                # self.database.add(support1)

                # chat1 = SupportChat(messages=json.dumps([{'sender': 'user', 'message': 'Здравствуйте! Помогите, как открыть карту?'}, {'sender': 'support', 'message': 'Здравствуйте! Для открытие карты просто выберите символ карты на панели внизу'}]), user=user_user.id, support=user_support.id)
                # self.database.add(chat1)

                review1_1 = Review(user_id=user_superadmin.id, partner_id=partner1.id, support_id=user_support1.id, rating=5, desc='Это не булочная — это искусство! Круассан с миндальной начинкой тает во рту, а кофе — как в Париже. Цены высоковаты, но оно того стоит.', state='published')
                review1_2 = Review(user_id=user_superadmin.id, partner_id=partner1.id, support_id=user_support1.id, rating=5, desc='Обожаю их лимонные тарты — кисло-сладкий баланс идеален. Персонал знает всё о каждом десерте. Единственный минус — трудно уйти без пяти коробок пирожных.', state='published')
                review1_3 = Review(user_id=user_superadmin.id, partner_id=partner1.id, support_id=user_support1.id, rating=4, desc='Вкусно, но очереди в выходные — как в мавзолей. Советую брать эклеры с утра: к вечеру выбор меньше. Бонусные баллы копятся приятно.', state='published')
                review1_4 = Review(user_id=user_superadmin.id, partner_id=partner1.id, support_id=user_support1.id, rating=3, desc='Хлеб — огонь, но пирожные часто приторные. Зачем портить идеальный бисквит тоннами сахарной глазури? Цены как в Цюрихе, а порции — как в советской столовой.', state='published')
                review1_5 = Review(user_id=user_superadmin.id, partner_id=partner1.id, support_id=user_support1.id, rating=1, desc='Купила «фирменный» багет — внутри сырое тесто. На претензию ответили: «Такова рецептура». Больше ногой не ступлю.', state='published')

                review2_1 = Review(user_id=user_superadmin.id, partner_id=partner2.id, support_id=user_support1.id, rating=2, desc='Было съедобно, но не более. Бургер холодный, соуса кот наплакал. Зато картошка нормальная, хоть и не досоленная. Персонал будто в замедленной съемке — ждал заказ 15 минут.', state='published')
                review2_2 = Review(user_id=user_superadmin.id, partner_id=partner2.id, support_id=user_support1.id, rating=1, desc='Whopper — полный провал! Мясо как подошва, овощи вялые, булка размокла. Еще и в зале грязно. Больше ни ногой сюда', state='published')
                review2_3 = Review(user_id=user_superadmin.id, partner_id=partner2.id, support_id=user_support1.id, rating=2, desc='Цены выросли, а порции уменьшились. Наггетсы жесткие, будто их трижды разогревали. Единственный плюс — скидки в приложении, но даже они не спасают.', state='published')
                review2_4 = Review(user_id=user_superadmin.id, partner_id=partner2.id, support_id=user_support1.id, rating=3, desc='Обычный фастфуд без восторгов. Бургер собрали криво, но хотя бы не забыли положить котлету. Кофе — просто коричневая вода. Место для экстренного перекуса, не более.', state='published')
                review2_5 = Review(user_id=user_superadmin.id, partner_id=partner2.id, support_id=user_support1.id, rating=0, desc='ПРОКЛЯТЫЙ ЧИЗБУРГЕР! Заказал два — оба были без сыра. Назовите это хоть как-то иначе, но не обманывайте людей! Теперь только конкуренты.', state='published')
                
                review3_1 = Review(user_id=user_superadmin.id, partner_id=partner3.id, support_id=user_support1.id, rating=5, desc='Это не магазин — книжный рай! Самый богатый ассортимент в городе, включая редкие издания. Персонал — настоящие эрудиты: посоветовали потрясающий роман, который теперь мой фаворит. Отдельное спасибо за уютное кафе с видом на книжные полки!', state='published')
                review3_2 = Review(user_id=user_superadmin.id, partner_id=partner3.id, support_id=user_support1.id, rating=5, desc='Каждый визит в «Буквоед» — праздник. Купила роскошное подарочное издание «Алисы в Стране чудес» с иллюстрациями Дали — такого нет даже в интернете! Дочка в восторге от детских мастер-классов: теперь читает взахлеб.', state='published')
                review3_3 = Review(user_id=user_superadmin.id, partner_id=partner3.id, support_id=user_support1.id, rating=5, desc='Лучший сервис! Заказал книгу с доставкой в другой город — пришла идеально упакованной, быстрее срока. В подарок положили закладку ручной работы и чайный пакетик. Мелочь, а приятно!', state='published')
                review3_4 = Review(user_id=user_superadmin.id, partner_id=partner3.id, support_id=user_support1.id, rating=5, desc='Здесь понимают книголюбов. Мне подписали книгу на мероприятии с автором, а потом предложили бесплатный кофе. Атмосфера такая, что хочется остаться на весь день. Цены адекватные для такого качества.', state='published')
                review3_5 = Review(user_id=user_superadmin.id, partner_id=partner3.id, support_id=user_support1.id, rating=5, desc='15 лет покупаю книги только здесь! Ни разу не разочаровался. Даже в пандемию организовали бесконтактную доставку с персональными рекомендациями. «Буквоед» — эталон книжной культуры!', state='published')
                
                review4_1 = Review(user_id=user_superadmin.id, partner_id=partner4.id, support_id=user_support1.id, rating=5, desc='Всегда полный ассортимент, вежливый персонал и хорошие цены. Особенно радует, что можно заказать редкие препараты с доставкой на дом. Спасибо за качественный сервис!', state='published')
                review4_2 = Review(user_id=user_superadmin.id, partner_id=partner4.id, support_id=user_support1.id, rating=4, desc='В целом доволен: цены нормальные, ассортимент широкий. Но однажды попался препарат с подходящим к концу сроком годности — пришлось возвращаться. Теперь всегда проверяю.', state='published')
                review4_3 = Review(user_id=user_superadmin.id, partner_id=partner4.id, support_id=user_support1.id, rating=4, desc='Аптека отличная, но в часы пик (утром и вечером) приходится ждать. Персонал старается, но не всегда справляется с наплывом. Зато есть онлайн-заказ — это спасает.', state='published')
                review4_4 = Review(user_id=user_superadmin.id, partner_id=partner4.id, support_id=user_support1.id, rating=3, desc='Недавно купила лекарство — оказалось дороже, чем в соседней аптеке. Фармацевт не смогла толком объяснить разницу в цене. Но выбор большой, и иногда попадаются выгодные акции.', state='published')
                review4_5 = Review(user_id=user_superadmin.id, partner_id=partner4.id, support_id=user_support1.id, rating=4, desc='Нравится система лояльности и скидки. Но вот доставка иногда задерживается — обещали за день, а привезли через два. В остальном — одна из лучших сетей.', state='published')
                
                review5_1 = Review(user_id=user_superadmin.id, partner_id=partner5.id, support_id=user_support1.id, rating=5, desc='Лучший бензин в городе! Двигатель работает ровно, расход меньше, чем на других АЗС. Еще люблю их кофе и выпечку — всегда свежие. Персонал вежливый, даже ночью!', state='published')
                review5_2 = Review(user_id=user_superadmin.id, partner_id=partner5.id, support_id=user_support1.id, rating=4, desc='Хорошая заправка, но цены выше среднего. Зато качество топлива стабильное, и магазин при АЗС — спасение в дороге. Минус — иногда долго ждешь кассира.', state='published')
                review5_3 = Review(user_id=user_superadmin.id, partner_id=partner5.id, support_id=user_support1.id, rating=3, desc='Нормально, но не более. Топливо качественное, но однажды попался недолив. Кафе часто закрыто на «технический перерыв». Бонусы по карте радуют, но копятся медленно.', state='published')
                review5_4 = Review(user_id=user_superadmin.id, partner_id=partner5.id, support_id=user_support1.id, rating=2, desc='Разочарован! Взял масло в магазине — оказалось просроченным. На претензию ответили: «Самостоятельно проверяйте сроки». Больше не рискую покупать что-то, кроме бензина.', state='published')
                review5_5 = Review(user_id=user_superadmin.id, partner_id=partner5.id, support_id=user_support1.id, rating=4, desc='Удобное расположение, чистота, есть мойка. Топливо дороже, чем у конкурентов, но двигатель не «стучит». Советую заправляться здесь в долгие поездки', state='published')
                
                review6_1 = Review(user_id=user_superadmin.id, partner_id=partner6.id, support_id=user_support1.id, rating=5, desc='Лучшая заправка в городе! Всегда свежее топливо, быстрая обслуживание, а кофе в магазине — просто бомба. Еще и бонусы на карту капают — мелочь, а приятно!', state='published')
                review6_2 = Review(user_id=user_superadmin.id, partner_id=partner6.id, support_id=user_support1.id, rating=5, desc='"Часто заправляюсь здесь — двигатель работает ровно, никаких проблем. Персонал вежливый, на кассах почти нет очередей. А еще люблю их хот-доги — неожиданно вкусно!', state='published')
                review6_3 = Review(user_id=user_superadmin.id, partner_id=partner6.id, support_id=user_support1.id, rating=4, desc='Хорошая АЗС, но в последний раз не работала мойка. Топливо качественное, цены нормальные, но хотелось бы больше акций на автохимию.', state='published')
                review6_4 = Review(user_id=user_superadmin.id, partner_id=partner6.id, support_id=user_support1.id, rating=3, desc='В целом нормально, но в магазине дороговато. Кофе мог бы быть и покрепче. Заправляюсь тут, потому что рядом с домом, но не более.', state='published')
                review6_5 = Review(user_id=user_superadmin.id, partner_id=partner6.id, support_id=user_support1.id, rating=2, desc='Однажды попалось топливо с водой — пришлось промывать бак. Больше не рискую, хоть и обещали компенсацию. Из плюсов — чистота на территории.', state='published')
                
                review7_1 = Review(user_id=user_superadmin.id, partner_id=partner7.id, support_id=user_support1.id, rating=5, desc='Всегда нахожу здесь даже редкие препараты, а фармацевты подсказывают аналоги дешевле. Еще люблю их косметические наборы со скидками — качественно и недорого!', state='published')
                review7_2 = Review(user_id=user_superadmin.id, partner_id=partner7.id, support_id=user_support1.id, rating=4, desc='Хороший выбор, но иногда задерживают заказы на 1–2 дня. Зато цены ниже, чем в соседних аптеках, и есть бонусная программа.', state='published')
                review7_3 = Review(user_id=user_superadmin.id, partner_id=partner7.id, support_id=user_support1.id, rating=3, desc='Нормально, но вечно нет свободных кассиров. Очереди утром и вечером — как в поликлинике. Зато есть всё, даже ортопедические стельки.', state='published')
                review7_4 = Review(user_id=user_superadmin.id, partner_id=partner7.id, support_id=user_support1.id, rating=2, desc='Дважды продавали лекарства с подходящим к концу сроком годности. Теперь всегда проверяю. Персонал не всегда дружелюбный.', state='published')
                review7_5 = Review(user_id=user_superadmin.id, partner_id=partner7.id, support_id=user_support1.id, rating=1, desc='Ждала заказ неделю, хотя обещали за 2 дня. В итоге пришлось искать в другой аптеке. Больше не рискую.', state='published')
                
                review8_1 = Review(user_id=user_superadmin.id, partner_id=partner8.id, support_id=user_support1.id, rating=5, desc='Люблю Перекрёсток за свежесть продуктов и акции! Особенно нравится выбор сыров и мясной нарезки. Персонал вежливый, цены адекватные. Всегда приятно заходить!', state='published')
                review8_2 = Review(user_id=user_superadmin.id, partner_id=partner8.id, support_id=user_support1.id, rating=3, desc='Магазин удобный, но иногда попадается просрочка среди молочки. Ассортимент хороший, но цены выше, чем в других сетях. В целом нормально, но есть куда расти.', state='published')
                review8_3 = Review(user_id=user_superadmin.id, partner_id=partner8.id, support_id=user_support1.id, rating=1, desc='Очереди вечно огромные, кассиры медленные. Купил вчера йогурт — оказался испорченным. Больше не хочу сюда возвращаться, лучше пойду в другой магазин.', state='published')
                review8_4 = Review(user_id=user_superadmin.id, partner_id=partner8.id, support_id=user_support1.id, rating=4, desc='Хороший магазин, но есть нюансы. Очень удобное расположение, большой выбор, но иногда не хватает свободных касс, и очереди скапливаются. Зато всегда есть скидки на сладости и кофе — это радует!', state='published')
                review8_5 = Review(user_id=user_superadmin.id, partner_id=partner8.id, support_id=user_support1.id, rating=5, desc='Мой любимый магазин! Всегда свежие овощи и фрукты, а отдел с готовой едой просто спасает после работы. Особенно нравятся их салаты и горячие курочки. Персонал приветливый, цены по акциям — просто сказка!', state='published')
                
                self.database.add(review1_1)
                self.database.add(review1_2)
                self.database.add(review1_3)
                self.database.add(review1_4)
                self.database.add(review1_5)
                self.database.add(review2_1)
                self.database.add(review2_2)
                self.database.add(review2_3)
                self.database.add(review2_4)
                self.database.add(review2_5)
                self.database.add(review3_1)
                self.database.add(review3_2)
                self.database.add(review3_3)
                self.database.add(review3_4)
                self.database.add(review3_5)
                self.database.add(review4_1)
                self.database.add(review4_2)
                self.database.add(review4_3)
                self.database.add(review4_4)
                self.database.add(review4_5)
                self.database.add(review5_1)
                self.database.add(review5_2)
                self.database.add(review5_3)
                self.database.add(review5_4)
                self.database.add(review5_5)
                self.database.add(review6_1)
                self.database.add(review6_2)
                self.database.add(review6_3)
                self.database.add(review6_4)
                self.database.add(review6_5)
                self.database.add(review7_1)
                self.database.add(review7_2)
                self.database.add(review7_3)
                self.database.add(review7_4)
                self.database.add(review7_5)
                self.database.add(review8_1)
                self.database.add(review8_2)
                self.database.add(review8_3)
                self.database.add(review8_4)
                self.database.add(review8_5)
                # review2 = Review(user_id=user_user.id, partner_id=partner1.id, support_id=user_support.id, rating=5, desc='кто же ожидал, что в буше такие вкусные яийчницы, точно не я', state='published')
                # self.database.add(review2)

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

            if session['saved_loc'] == 'false':
                user_input = ''
            if user_input != '':
                locations = search_closest_locations(session['lat'], session['lon'], user_input)
                return render_template('user/map.html', locations=locations, key=settings.TWOGIS_API_KEY)
            return render_template('user/map.html', locations=[], key=settings.TWOGIS_API_KEY)


        # flask support callback function
        @self.flask.route('/user/support', methods=['GET', 'POST'])
        def support():
            if request.method == 'POST':
                if not self.database.get('SupportChat', 'user', session['user_id']):
                    support = self.database.get('User', 'type', 'Support')
                    self.next_support = self.next_support % len(support)
                    support = support[self.next_support]
                    self.next_support += 1
                    chat = SupportChat(messages='[]', user=session['user_id'], support=support.id)
                    self.database.add(chat)

            user_info = self.database.get_one('User', 'id', session['user_id'])
            
            chat = self.database.get('SupportChat', 'user', user_info.id)

            if len(chat) == 0:
                # chat = SupportChat(messages='[]', user=user_info.id, support=0)
                # self.database.add(chat)
                return render_template('user/support.html', user=user_info, user_id=user_info.id, messages='[]', chat_exist=False)
    
            chat = chat[0]
            support_id = chat.support
            return render_template('user/support.html', user=user_info, user_id=user_info.id, support_id=support_id, messages=json.loads(chat.messages), chat_exist=True)

        # main page callback function
        @self.flask.route('/user/home', methods=['GET', 'POST'])
        def home():
            session['prev_page'] = 'home'

            user = self.database.get_one('User', 'id', session['user_id'])
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
            user = self.database.get_one('User', 'id', session['user_id'])

            last_partners = json.loads(user.last_partners)
            last_partners = [partner.id] + [i for i in last_partners if i != partner.id]
            user.last_partners = json.dumps(last_partners)
            self.database.update(user)

            return render_template('user/partner.html', partner=partner)

        # partner reviews page flask callback function
        @self.flask.route('/user/reviews', methods=['POST'])
        def reviews():
            partner_id = 0

            if 'review_button' in request.form:
                partner_id = request.form['review_button']
            else:
                partner_id = request.form['partner_id']
                desc = request.form['desc']
                rating = float(request.form['rating'])
                support = self.database.get('User', 'type', 'Support')
                self.next_support = self.next_support % len(support)
                support = support[self.next_support]
                self.next_support += 1
                state = 'approval'
                if desc == '':
                    partner = self.database.get_one('Partner', 'id', partner_id)
                    comments = self.database.get('Review', 'partner_id', partner_id)
                    comments = [i for i in comments if i.state == 'published']
                    n = len(comments)

                    partner.rating = (partner.rating * (n) + rating) / (n + 1)
                    self.database.update(partner)
                    state = 'published'

                comment = Review(user_id=session['user_id'], partner_id=partner_id, support_id=support.id, rating=rating, desc=desc, state=state)
                self.database.add(comment)
            
            comments = self.database.get('Review', 'partner_id', partner_id)
            comments = [i for i in comments if i.state == 'published']
            size = len(comments)
            for i in range(0, size):
                local_user = self.database.get_one('User', 'id', comments[i].user_id)
                comments[i] = {
                    'rating': comments[i].rating, 
                    'desc': comments[i].desc,
                    'user_name': local_user.name,
                    'user_age': (datetime.datetime.now().date() - local_user.birthday).days // 365
                    }
            return render_template('user/reviews.html', comments=comments, partner_id=partner_id)

        # getting back from partner page flask callback function
        @self.flask.route('/user/back', methods=['GET'])
        def partner_back():
            return redirect(url_for(session['prev_page']), 301)

        # flask user profile callback function
        @self.flask.route('/user/profile', methods=['GET', 'POST'])
        def profile():
            user = self.database.get_one('User', 'id', session['user_id'])
            if request.method == 'POST':
                user.telegram = request.form['telegram-field']
                user.birthday = datetime.datetime.strptime(request.form['birthday-field'], '%Y-%m-%d')
                user.email = request.form['email-field']
                self.database.update(user)

            return render_template('user/profile.html', user=user)

        # flask user profile callback function
        @self.flask.route('/user/profile_edit', methods=['GET'])
        def profile_edit():
            return render_template('user/profile_edit.html', user=self.database.get_one('User', 'id', session['user_id']))


        ### flask inner callback functions ###

        # user location saving function
        @self.flask.route('/save_user_location/<float:lat>/<float:lon>', methods=['POST'])
        def save_user_location(lat, lon):
            session['lat'] = lat
            session['lon'] = lon
            session['saved_loc'] = 'true'
            return '', 204
        
        # flask socket io handling function
        @self.socketio.on('message')
        def handle_message(msg):
            user_id = 0
            if json.loads(msg)['sender_type'] == 'user':
                user_id = json.loads(msg)['sender']
            else:
                user_id = json.loads(msg)['receiver']
            chat = self.database.get_one('SupportChat', 'user', user_id)
            
            if chat:
                new_messages = json.loads(chat.messages)
                new_messages.append({'sender': json.loads(msg)['sender_type'], 'message': json.loads(msg)['text']})
                chat.messages = json.dumps(new_messages)
                self.database.update(chat)

            if json.loads(msg)['text'] == '~EndConvo~':
                self.database.delete('SupportChat', chat.id)
                emit('redirect', {'url': url_for('support'), 'user_id': user_id})
            emit('message', msg, broadcast=True)

        
        ### admin role flask callback functions ### 

        # roles management flask callback function
        @self.flask.route('/admin/roles', methods=['GET'])
        def admin_roles():
            user = self.database.get_one('User', 'id', session['user_id'])
            if not(user.type in ['Superadmin', 'Admin', 'Director', 'Support']):
                return render_template('error.html')     
            return render_template('admin/roles.html', user=user, users=self.database.get_sort('User', 'name', 100))
                
        
        # parter page flask callback function
        @self.flask.route('/admin/partner', methods=['POST', 'GET'])
        def admin_partner():
            user = self.database.get_one('User', 'id', session['user_id'])
            if not(user.type in ['Director', 'Manager']):
                return render_template('error.html')
            partner = self.database.get_one('Partner', 'director_id', user.id)
            if partner == None:
                partner = Partner(director_id=user.id, rating=0)
            if request.method == 'POST':
                for attr in ['name', 'type', 'org_id', 'logo_url', 'image_urls', 'info']:
                    setattr(partner, attr, request.form[attr])
                sales_amounts = [int(i.split('%')[0]) for i in request.form['sales'].split('\n')]
                sales_descs = [i.split('%')[1] for i in request.form['sales'].split('\n')]
                partner.best_sale_amount = max(sales_amounts)
                sales = '\n'.join(['%'.join([str(sales_amounts[i]), sales_descs[i]]) for i in range(len(sales_amounts))])
                partner.sales = sales
                if partner.id == None:
                    self.database.add(partner)
                else:
                    self.database.update(partner)
            return render_template('admin/partner.html', user=user, partner=partner)
        

        # support flask callback function
        @self.flask.route('/admin/support', methods=['GET'])
        def admin_support():
            user = self.database.get_one('User', 'id', session['user_id'])
            if not(user.type in ['Support']):      
                return render_template('error.html') 
            return render_template('admin/support.html', user=user)


        ### manager flask callback functions ###

        @self.flask.route('/manager/reviews', methods=['GET'])
        def manager_reviews():

            return render_template('manager/reviews.html')


        ### support flask callback functions ###

        # supports reviews checking page flask callback function
        @self.flask.route('/support/reviews', methods=['GET', 'POST'])
        def support_reviews():
            if request.method == 'POST':
                comment = self.database.get_one('Review', 'id', request.form['comment_id'])
                if request.form['button'] == 'publish':
                    comment.state = 'published'
                    partner = self.database.get_one('Partner', 'id', comment.partner_id)
                    comments = self.database.get('Review', 'partner_id', partner.id)
                    comments = [i for i in comments if i.state == 'published']
                    n = len(comments)

                    partner.rating = (partner.rating * (n) + comment.rating) / (n + 1)
                    self.database.update(partner)
                else:
                    comment.state = 'denied'
                self.database.update(comment)

            comments = self.database.get('Review', 'support_id', session['user_id'])
            comments = [i for i in comments if i.state == 'approval']
            size = len(comments)
            for i in range(0, size):
                local_user = self.database.get_one('User', 'id', comments[i].user_id)
                comments[i] = {
                    'rating': comments[i].rating, 
                    'desc': comments[i].desc,
                    'user_name': local_user.name,
                    'user_age': (datetime.datetime.now().date() - local_user.birthday).days // 365,
                    'id': comments[i].id
                    }
            return render_template('support/reviews.html', comments=comments)

        # chats for supports page flask callback function
        @self.flask.route('/support/chats', methods=['GET', 'POST'])
        def support_chats():
            chats = self.database.get('SupportChat', 'support', session['user_id'])
            headers = []
            
            i = 0
            # print(chats)
            for chat in chats:
                messages = json.loads(chat.messages)
                last_message = 'Пока сообщений нет'
                if len(messages) > 0:
                    last_message = messages[len(messages) - 1]
                user = self.database.get_one('User', 'id', chat.user)
                headers.append({
                    'chat_id': i,
                    'user_name': user.name,
                    'last_message': last_message
                })
                i += 1
            nochats = True
            messages = []
            user_id = 0
            if len(chats) > 0:
                ind = 0
                if request.method == 'POST':
                    ind = int(request.form['chatButton'])
                if ind >= len(chats):
                    return render_template('support/chats.html', headers=headers, messages=messages, nochats=nochats, user_id=user_id, support_id=session['user_id'])

                messages = json.loads(chats[ind].messages)
                user_id = chats[ind].user
                nochats = False
            return render_template('support/chats.html', headers=headers, messages=messages, nochats=nochats, user_id=user_id, support_id=session['user_id'])


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
                    'key': settings.TWOGIS_API_KEY,
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