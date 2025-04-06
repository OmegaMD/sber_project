# Database library, to import use "from database.py import *"
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc


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

    # User adding function
    def add(self, entity):
        DataBase.db.session.add(entity)
        DataBase.db.session.commit()

    # User deleting function
    def delete(self, type, id):
        DataBase.db.session.delete(globals()[type].query.filter_by(id=id).one())
        DataBase.db.session.commit()

    # User getting function
    def get(self, type, filter_field, filter_data):
        return globals()[type].query.filter_by(**{filter_field: filter_data}).all()
    
    # Get top sorted rows
    def get_sort(self, type, sort_field, num):
        return globals()[type].query.order_by(desc(DataBase.db.text(type + "." + sort_field))).limit(num).all()

    # User updating function
    def update(self, entity):
        old_entity = entity.query.filter_by(id=entity.id).one()
        for var in vars(old_entity).keys():
            setattr(old_entity, var, getattr(entity, var))
        DataBase.db.session.commit()


# Users table model
class User(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    name = DataBase.db.Column(DataBase.db.String, nullable=False)
    email = DataBase.db.Column(DataBase.db.String, unique=True, nullable=False)
    telegram = DataBase.db.Column(DataBase.db.String, unique=True, nullable=False)

# Partner table model
class Partner(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    type = DataBase.db.Column(DataBase.db.String, nullable=False)
    name = DataBase.db.Column(DataBase.db.String, nullable=False)
    image_url = DataBase.db.Column(DataBase.db.String, nullable=False)
    logo_url = DataBase.db.Column(DataBase.db.String)
    org_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)