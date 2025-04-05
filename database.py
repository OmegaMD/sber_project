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
    def get_sort(self, type, filter_field, num):
        return globals()[type].query.order_by(desc(DataBase.db.text(type + "." + filter_field))).limit(num).all()

    # User updating function
    def update_user(self, entity):
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


class Partner(DataBase.db.Model):
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, unique=True, nullable=False)
    type = DataBase.db.Column(DataBase.db.String, nullable=False)
    name = DataBase.db.Column(DataBase.db.String, nullable=False)
    image_url = DataBase.db.Column(DataBase.db.String, nullable=False)
    logo_url = DataBase.db.Column(DataBase.db.String)
    org_id = DataBase.db.Column(DataBase.db.Integer, nullable=False)

"""
# Initialize the Flask application
app = Flask(__name__)

database = DataBase(app, 'data.db')

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    database.start()
    if User.query.count() == 0:
        user_a = User(name='Alice', email='alice@example.com', telegram='@Alice')
        user_b = User(name='Bob', email='bob@example.com', telegram='@Bob')
        user_c = User(name='Charlie', email='charlie@example.com', telegram='@Charlie')
        database.add(user_a)
        database.add(user_b)
        database.add(user_c)
        Partner_a = Partner(type='Кондиитер ёбаный', name='У Михалыча', image_url='run_the_gauntlet.png', logo_url='FUCK', org_id=1337)
        database.add(Partner_a)

    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email, 'telegram': user.telegram} for user in users])

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
"""