from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy import *
from sqlalchemy.engine import reflection
# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turn off Flask-SQLAlchemy modification tracking
db = SQLAlchemy(app)

# Define a model for the database
class Users(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.user_name}>'

class Partners(db.Model):
    partner_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    partner_name = db.Column(db.String(100), nullable=False)
    img_sizex = db.Column(db.Integer, nullable=False)
    img_sizey = db.Column(db.Integer, nullable=False)
    partner_img = db.Column(db.String(1000), nullable=False)
    partner_type = db.Column(db.String(120), nullable=False)
    partner_website = db.Column(db.String(100))
    partner_phone = db.Column(db.String(100))
    partner_description = db.Column(db.String(1000))

    def __repr__(self):
        return f'<Partner {self.partner_name}>'

class Places(db.Model):
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    place_partner = db.Column(db.String, ForeignKey(Partners.partner_id), nullable=False)
    place_adress = db.Column(db.String(150), nullable=False)
    place_latitude = db.Column(db.String(150), nullable=False)
    place_longitude = db.Column(db.String(150), nullable=False)

class Reviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rewiew_user = db.Column(db.Integer, ForeignKey(Users.user_id), nullable=False)
    rewiew_place = db.Column(db.Integer, ForeignKey(Places.place_id), nullable=False)
    rewiew_contents = db.Column(db.String(2000), nullable=False)

class Sales(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_partner = db.Column(db.String, ForeignKey(Partners.partner_id), nullable=False)
    sale_amount = db.Column(db.String(100), nullable=False)
    sale_description = db.Column(db.String(1000), nullable=False)

class Rights(db.Model):
    right_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(30), nullable=False)
    rights_userid = db.Column(db.Integer, ForeignKey(Users.user_id))
    rights_partner = db.Column(db.Integer, ForeignKey(Partners.partner_id))
    rights_place = db.Column(db.Integer, ForeignKey(Places.place_id))

    

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
