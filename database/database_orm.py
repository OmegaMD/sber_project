from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy import *
from sqlalchemy.engine import reflection


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turn off Flask-SQLAlchemy modification tracking
db = SQLAlchemy(app)    


class User:
    def __init__(self, id, telegram_id, name, surname, email):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.telegram_id = telegram_id
    def __init__(self, result):
        self.id = result['id']
        self.name = result['name']
        self.surname = result['surname']
        self.email = result['email']
        self.telegram_id = result['telegram']

class Users(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

def create_user(user):
    insert(Users).values(id = user.id, telegram_id = user.telegram_id, name = user.name, surname = user.surname, email = user.email)

def remove_user(user_id):
    delete(Users).where(id = user_id)

def update_user(user):
    update(Users).where(id = user.id).values(telegram_id = user.telegram_id, name = user.name, surname = user.surname, email = user.email)

def get_user(user_id):
    return User(db.session.execute(db.select(User).filter_by(user_id = user_id)).scalar_one())


'''
class Partners(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    logo_url = db.Column(db.String(1000), nullable=False)
    website_url = db.Column(db.String(1000))
    phone = db.Column(db.String(20))
    description = db.Column(db.String(1000))


class Places(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    partner = db.Column(db.String, ForeignKey(Partners.partner_id), nullable=False)
    adress = db.Column(db.String(100), nullable=False)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey(Users.user_id), nullable=False)
    place_id = db.Column(db.Integer, ForeignKey(Places.place_id), nullable=False)
    content = db.Column(db.String(2000), nullable=False)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partner = db.Column(db.String, ForeignKey(Partners.partner_id), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)


class Rights(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    type = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(Users.user_id))
    partner = db.Column(db.Integer, ForeignKey(Partners.partner_id))

    
# Initialize the database (this will create the 'example.db' file)
with app.app_context():
    db.create_all()
    inspector = reflection.Inspector.from_engine(db.engine)
    if not inspector.has_table("partners"):
        # Сохранение изменений в базе данных
        db.session.commit()


# Home route to show users
@app.route('/')
def index():
    users = Users.query.all()  # Get all users from the database
    return render_template('index.html', users = users)

# Route to add a user
@app.route('/add', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = Users(user_name=name, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return str(e)
    
    return render_template('add_user.html')

def add_partner(name, imgx, imgy, img, type, website, phone , description):
    insert(Partners).values(partner_name = name, img_sizex = imgx, img_sizey = imgy, partner_img = img, partner_type = type, partner_website = website, partner_phone = phone, partner_description = description)

def set_rights(userid, newtype, newpartner, newplace):
    update(Rights).where(Rights.rights_userid == userid).values(type = newtype, rights_partner = newpartner, rights_place = newplace)

def add_place(partner, adress, latitude, longitude):
    insert(Places).values(place_parter = partner, place_adress = adress, place_latitude = latitude, place_longitude = longitude)

def add_sale(partner, amount, description):
    insert(Sales).values(sale_partner =  partner, sale_amount = amount, sale_description = description)

def remove_user(userid):
    delete(Users).where(user_id = userid)

def remove_partner(partnerid):
    delete(Partners).where(partner_id = partnerid)

def remove_place(placeid):
    delete(Places).where(place_id = placeid)

def remove_sale(saleid):
    delete(Sales).where(sale_id = saleid)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
'''