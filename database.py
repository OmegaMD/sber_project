# Database library, to import use "from database.py import *"
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

import json
from json import JSONEncoder


# Main Database controling class
class DataBase:
    # Database controller
    db = SQLAlchemy()

    # DataBase class initialization function (file_dir must end with .db)
    def __init__(self, flask_app, file_dir):
        # setting up flask app to work with database
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_dir

        # database controller initializer
        DataBase.db.init_app(flask_app)

    # Database starting function, should be called in one of the flasks callbacks
    def start(self):
        DataBase.db.create_all()

    # Data adding function
    def add(self, entity):
        DataBase.db.session.add(entity)
        DataBase.db.session.commit()

    # Data deleting function
    def delete(self, type, id):
        DataBase.db.session.delete(globals()[type].query.filter_by(id=id).one())
        DataBase.db.session.commit()

    # Data getting function
    def get(self, type, filter_field, filter_data):
        return globals()[type].query.filter_by(**{filter_field: filter_data}).all()
    
    # Getting one item function
    def get_one(self, type, filter_field, filter_data):
        response = self.get(type, filter_field, filter_data)
        if len(response) > 0:
            return response[0]
        else:
            return None

    # Get top sorted rows
    def get_sort(self, type, sort_field, num):
        return globals()[type].query.order_by(desc(DataBase.db.text(type + "." + sort_field))).limit(num).all()

    # Data updating function
    def update(self, entity):
        old_entity = entity.query.filter_by(id=entity.id).one()
        for var in vars(old_entity).keys():
            setattr(old_entity, var, getattr(entity, var))
        DataBase.db.session.commit()

# Sale base storing class
class Sale:
    def __init__(self, amount, desc):
        self.amount = amount
        self.desc = desc

# Sales json encoder
class SaleEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


# Users table model
class User(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    type = DataBase.db.Column(DataBase.db.String, nullable=False)
    name = DataBase.db.Column(DataBase.db.String, nullable=False)
    email = DataBase.db.Column(DataBase.db.String, nullable=False)
    telegram = DataBase.db.Column(DataBase.db.String, unique=True, nullable=False)
    birthday = DataBase.db.Column(DataBase.db.Date, nullable=False) 
    last_partners = DataBase.db.Column(DataBase.db.String, nullable=False)
    

# Partner table model
class Partner(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    director_id = DataBase.db.Column(DataBase.db.Integer, nullable=True)
    type = DataBase.db.Column(DataBase.db.String, nullable=False)
    name = DataBase.db.Column(DataBase.db.String, nullable=False)
    image_urls = DataBase.db.Column(DataBase.db.String, nullable=False)
    logo_url = DataBase.db.Column(DataBase.db.String, nullable=False)
    org_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)
    sales = DataBase.db.Column(DataBase.db.String, nullable=False)
    rating = DataBase.db.Column(DataBase.db.Float, nullable=False)
    info = DataBase.db.Column(DataBase.db.String, nullable=False)
    best_sale_amount = DataBase.db.Column(DataBase.db.Integer, nullable=False)


# Review table models
class Review(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)
    partner_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)
    support_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)
    # reply_review_id = DataBase.db.Column(DataBase.db.Integer)
    rating = DataBase.db.Column(DataBase.db.Integer, nullable=False)
    desc = DataBase.db.Column(DataBase.db.String)
    state = DataBase.db.Column(DataBase.db.String, nullable=False)


# Supports list table model
class Support(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)


# Managers list table model
class Manager(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)
    partner_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)


# Support chats table model
class SupportChat(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    messages = DataBase.db.Column(DataBase.db.String)
    user = DataBase.db.Column(DataBase.db.Integer, nullable=False)
    support = DataBase.db.Column(DataBase.db.Integer, nullable=False)