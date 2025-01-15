from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turn off Flask-SQLAlchemy modification tracking
db = SQLAlchemy(app)

# Define a model for the database
'''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    name = db.Column(db.String(100), nullable=False)  # User's name
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email

    def __repr__(self):
        return f'<User {self.name}>'
'''

class Partner(db.Model):
    partner_name = db.Column(db.String(100), unique = True, nullable = False, primary_key = True)
    img_sizex = db.Column(db.Integer, nullable = False)
    img_sizey = db.Column(db.Integer, nullable = False)
    partner_img = db.Column(db.String(1000), nullable = False)
    partner_type = db.Column(db.String(120), nullable = False)

    def __repr__(self):
        return f'<Partner {self.partner_name}>'

def add_partners():
    # Пример добавления данных
    partner1 = Partner(partner_name = "мега", 
                    img_sizex = 50,
                    img_sizey = 15,
                    partner_img = 'https:upload.wikimedia.org/wikipedia/ru/7/7a/Logo_mega.gif',
                    partner_type = "supermarket")

    # Добавление пользователей в сессию
    db.session.add(partner1)
    
    # Сохранение изменений в базе данных
    db.session.commit()


# Initialize the database (this will create the 'example.db' file)
with app.app_context():
    db.create_all()
    add_partners()

# Home route to show users
@app.route('/')
def index():
    users = User.query.all()  # Get all users from the database
    return render_template('index.html', users=users)

# Route to add a user
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = User(name=name, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the user'
    
    return render_template('add_user.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
