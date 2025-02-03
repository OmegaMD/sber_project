from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
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
    rights = db.Column(db.String(50), nullable=False, default="user")  # Убираем unique=True
    def __repr__(self):
        return f'<User {self.user_name}>'

class Partners(db.Model):
    partner_name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    img_sizex = db.Column(db.Integer, nullable=False)
    img_sizey = db.Column(db.Integer, nullable=False)
    partner_img = db.Column(db.String(1000), nullable=False)
    partner_type = db.Column(db.String(120), nullable=False)
    partner_contacts = db.Column(db.String(100))
    partner_description = db.Column(db.String(1000))

    def __repr__(self):
        return f'<Partner {self.partner_name}>'

def add_partners():
    # Пример добавления данных
    partner1 = Partners(partner_name = "мега", 
                    img_sizex = 50,
                    img_sizey = 15,
                    partner_img = 'https:upload.wikimedia.org/wikipedia/ru/7/7a/Logo_mega.gif',
                    partner_type = "supermarket")

    # Добавление пользователей в сессию
    db.session.add(partner1)

class Places(db.Model):
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    partner = db.Column(db.String, ForeignKey(Partners.partner_name), nullable=False)
    adress = db.Column(db.String(150), nullable=False)

class Reviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, ForeignKey(Users.user_id), nullable=False)
    place = db.Column(db.Integer, ForeignKey(Places.place_id), nullable=False)
    Contents = db.Column(db.String(2000), nullable=False)

class Sales(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partner = db.Column(db.String, ForeignKey(Partners.partner_name), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

# Initialize the database (this will create the 'example.db' file)
with app.app_context():
    db.create_all()
    inspector = reflection.Inspector.from_engine(db.engine)
    if not inspector.has_table("partners"):
        add_partners()
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
