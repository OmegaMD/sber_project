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
    return User(db.session.execute(db.select(User).filter_by(id = user_id)).scalar_one())



class Partners(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    logo_url = db.Column(db.String(1000), nullable=False)
    website_url = db.Column(db.String(1000))
    phone = db.Column(db.String(20))
    description = db.Column(db.String(1000))

class Partner:
    def __init__(self, id, name, type, img_url, logo_url, website_url, phone, description):
        self.id = id
        self.name = name
        self.type = type
        self.img_url = img_url
        self.logo_url = logo_url
        self.website_url = website_url
        self.phone = phone
        self.description = description

    def __init__(self, result):  # Overloaded __init__ from dictionary
        self.id = result['id']
        self.name = result['name']
        self.type = result['type']
        self.img_url = result['img_url']
        self.logo_url = result['logo_url']
        self.website_url = result['website_url']
        self.phone = result['phone']
        self.description = result['description']

def create_partner(partner):
    insert(Partners).values(id = partner.id, name = partner.name, type = partner.type, img_url = partner.img_url, logo_url = partner.logo_url, website_url = partner.website_url, phone = partner.phone, description = partner.description)

def remove_partner(partner_id):
    delete(Partners).where(id = partner_id)

def update_partner(partner):
    update(Partners).where(id = partner.id).values(name = partner.name, type = partner.type, img_url = partner.img_url, logo_url = partner.logo_url, website_url = partner.website_url, phone = partner.phone, description = partner.description)

def get_partner(partner_id):
    return Partner(db.session.execute(db.select(Partner).filter_by(id = partner_id)).scalar_one())



class Places(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    partner = db.Column(db.String, ForeignKey(Partners.id), nullable=False)
    adress = db.Column(db.String(100), nullable=False)

class Place:
    def __init__(self, id, partner, adress):
        self.id = id
        self.partner = partner
        self.adress = adress

    def __init__(self, result):
        self.id = result['id']
        self.partner = result['partner']
        self.adress = result['adress']




class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey(Users.id), nullable=False)
    place_id = db.Column(db.Integer, ForeignKey(Places.id), nullable=False)
    content = db.Column(db.String(2000), nullable=False)

class Review:
    def __init__(self, id, user_id, place_id, content):
        self.id = id
        self.user_id = user_id
        self.place_id = place_id
        self.content = content

    def __init__(self, result):
        self.id = result['id']
        self.user_id = result['user_id']
        self.place_id = result['place_id']
        self.content = result['content']

def create_review(review):
    insert(Reviews).values(id = review.id, user_id = review.user_id, place_id = review.place_id, content = review.content)

def remove_review(review_id):
    delete(Reviews).where(id = review_id)

def update_review(review):
    update(Reviews).where(id = review.id).values(user_id = review.user_id, place_id = review.place_id, content = review.content)

def get_review(review_id):
    return Review(db.session.execute(db.select(Review).filter_by(id = review_id)).scalar_one())



class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partner = db.Column(db.String, ForeignKey(Partners.id), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

class Sale:
    def __init__(self, id, partner, amount, description):
        self.id = id
        self.partner = partner
        self.amount = amount
        self.description = description

    def __init__(self, result):
        self.id = result['id']
        self.partner = result['partner']
        self.amount = result['amount']
        self.description = result['description']

def create_sale(sale):
    insert(Sales).values(id = sale.id, partner = sale.partner, amount = sale.amount, description = sale.description)

def remove_sale(sale_id):
    delete(Sales).where(id = sale_id)

def update_sale(sale):
    update(Sales).where(id = sale.id).values(partner = sale.partner, amount = sale.amount, description = sale.description)

def get_sale(sale_id):
    return Sale(db.session.execute(db.select(Sale).filter_by(id = sale_id)).scalar_one())



class Rights(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    type = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(Users.id))
    partner = db.Column(db.Integer, ForeignKey(Partners.id))

class Right:
    def __init__(self, id, type, user_id, partner):
        self.id = id
        self.type = type
        self.user_id = user_id
        self.partner = partner

    def __init__(self, result):
        self.id = result['id']
        self.type = result['type']
        self.user_id = result['user_id']
        self.partner = result['partner']

def create_right(right):
    insert(Rights).values(id = right.id, type = right.type, user_id = right.user_id, partner = right.partner)

def remove_right(right_id):
    delete(Rights).where(id = right_id)

def update_right(right):
    update(Rights).where(id = right.id).values(type = right.type, user_id = right.user_id, partner = right.partner)

def get_right(right_id):
    return Right(db.session.execute(db.select(Right).filter_by(id = right_id)).scalar_one())


'''
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
    return render_template('index.html', users = users)'


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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
'''
