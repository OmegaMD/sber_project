from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *



class User:
    def __init__(self, id, telegram_id, name, surname, email):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.telegram_id = telegram_id

    def __init__(self, result): # Overloaded __init__ from dictionary
        self.id = result['id']
        self.name = result['name']
        self.surname = result['surname']
        self.email = result['email']
        self.telegram_id = result['telegram_id']



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

    def __init__(self, result): # Overloaded __init__ from dictionary
        self.id = result['id']
        self.name = result['name']
        self.type = result['type']
        self.img_url = result['img_url']
        self.logo_url = result['logo_url']
        self.website_url = result['website_url']
        self.phone = result['phone']
        self.description = result['description']



class Sale:
    def __init__(self, id, partner, amount, description):
        self.id = id
        self.partner = partner
        self.amount = amount
        self.description = description

    def __init__(self, result): # Overloaded __init__ from dictionary
        self.id = result['id']
        self.partner = result['partner']
        self.amount = result['amount']
        self.description = result['description']



class Review:
    def __init__(self, id, user_id, partner_id, content):
        self.id = id
        self.user_id = user_id
        self.partner_id = partner_id
        self.content = content

    def __init__(self, result): # Overloaded __init__ from dictionary
        self.id = result['id']
        self.user_id = result['user_id']
        self.partner_id = result['partner_id']
        self.content = result['content']



class Right:
    def __init__(self, id, type, user_id, partner):
        self.id = id
        self.type = type
        self.user_id = user_id
        self.partner = partner

    def __init__(self, result): # Overloaded __init__ from dictionary
        self.id = result['id']
        self.type = result['type']
        self.user_id = result['user_id']
        self.partner_id = result['partner_id']



class SQLA:
    def __init__(self, flask_app):
        self.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
        self.flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turn off Flask-SQLAlchemy modification tracking
        self.db = SQLAlchemy(flask_app)



class UsersTable(SQLA.db.Model):
    id = SQLA.db.Column(SQLA.db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    name = SQLA.db.Column(SQLA.db.String(100), nullable=False)
    surname = SQLA.db.Column(SQLA.db.String(100), nullable=False)
    email = SQLA.db.Column(SQLA.db.String(100), nullable=False, unique=True)

def create_user(user):
    insert(UsersTable).values(id = user.id, telegram_id = user.telegram_id, name = user.name, surname = user.surname, email = user.email)

def remove_user(user_id):
    delete(UsersTable).where(id = user_id)

def update_user(user):
    update(UsersTable).where(id = user.id).values(telegram_id = user.telegram_id, name = user.name, surname = user.surname, email = user.email)

def get_user(user_id):
    return User(SQLA.db.session.execute(SQLA.db.select(User).filter_by(id = user_id)).scalar_one())


 
class PartnersTable(SQLA.db.Model):
    id = SQLA.db.Column(SQLA.db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = SQLA.db.Column(SQLA.db.String(100), nullable=False)
    type = SQLA.db.Column(SQLA.db.String(100), nullable=False)
    img_url = SQLA.db.Column(SQLA.db.String(1000), nullable=False)
    logo_url = SQLA.db.Column(SQLA.db.String(1000), nullable=False)
    website_url = SQLA.db.Column(SQLA.db.String(1000))
    phone = SQLA.db.Column(SQLA.db.String(20))
    description = SQLA.db.Column(SQLA.db.String(1000))

def create_partner(partner):
    insert(PartnersTable).values(id = partner.id, name = partner.name, type = partner.type, img_url = partner.img_url, logo_url = partner.logo_url, website_url = partner.website_url, phone = partner.phone, description = partner.description)

def remove_partner(partner_id):
    delete(PartnersTable).where(id = partner_id)

def update_partner(partner):
    update(PartnersTable).where(id = partner.id).values(name = partner.name, type = partner.type, img_url = partner.img_url, logo_url = partner.logo_url, website_url = partner.website_url, phone = partner.phone, description = partner.description)

def get_partner(partner_id):
    return Partner(SQLA.db.session.execute(SQLA.db.select(Partner).filter_by(id = partner_id)).scalar_one())



class ReviewsTable(SQLA.db.Model):
    id = SQLA.db.Column(SQLA.db.Integer, primary_key=True, autoincrement=True)
    user_id = SQLA.db.Column(SQLA.db.Integer, ForeignKey(UsersTable.id), nullable=False)
    partner_id = SQLA.db.Column(SQLA.db.Integer, ForeignKey(PartnersTable.id), nullable=False)
    content = SQLA.db.Column(SQLA.db.String(2000), nullable=False)

def create_review(review):
    insert(ReviewsTable).values(id = review.id, user_id = review.user_id, place_id = review.place_id, content = review.content)

def remove_review(review_id):
    delete(ReviewsTable).where(id = review_id)

def update_review(review):
    update(ReviewsTable).where(id = review.id).values(user_id = review.user_id, place_id = review.place_id, content = review.content)

def get_review(review_id):
    return Review(SQLA.db.session.execute(SQLA.db.select(Review).filter_by(id = review_id)).scalar_one())



class SalesTable(SQLA.db.Model):
    id = SQLA.db.Column(SQLA.db.Integer, primary_key=True, autoincrement=True)
    partner = SQLA.db.Column(SQLA.db.String, ForeignKey(PartnersTable.id), nullable=False)
    amount = SQLA.db.Column(SQLA.db.String(100), nullable=False)
    description = SQLA.db.Column(SQLA.db.String(1000), nullable=False)

def create_sale(sale):
    insert(SalesTable).values(id = sale.id, partner = sale.partner, amount = sale.amount, description = sale.description)

def remove_sale(sale_id):
    delete(SalesTable).where(id = sale_id)

def update_sale(sale):
    update(SalesTable).where(id = sale.id).values(partner = sale.partner, amount = sale.amount, description = sale.description)

def get_sale(sale_id):
    return Sale(SQLA.db.session.execute(SQLA.db.select(Sale).filter_by(id = sale_id)).scalar_one())



class RightsTable(SQLA.db.Model):
    id = SQLA.db.Column(SQLA.db.Integer, nullable=False, primary_key=True, autoincrement=True)
    type = SQLA.db.Column(SQLA.db.String(30), nullable=False)
    user_id = SQLA.db.Column(SQLA.db.Integer, ForeignKey(UsersTable.id))
    partner_id = SQLA.db.Column(SQLA.db.Integer, ForeignKey(PartnersTable.id))

def create_right(right):
    insert(RightsTable).values(id = right.id, type = right.type, user_id = right.user_id, partner = right.partner_id)

def remove_right(right_id):
    delete(RightsTable).where(id = right_id)

def update_right(right):
    update(RightsTable).where(id = right.id).values(type = right.type, user_id = right.user_id, partner = right.partner_id)

def get_right(right_id):
    return Right(SQLA.db.session.execute(SQLA.db.select(Right).filter_by(id = right_id)).scalar_one())



'''
# Initialize the database (this will create the 'example.db' file)
with app.app_context():
    SQLA.db.create_all()
    inspector = reflection.Inspector.from_engine(SQLA.db.engine)
    if not inspector.has_table("partners"):
        # Сохранение изменений в базе данных
        SQLA.db.session.commit()


# Home route to show users
@app.route('/')
def index():
    users = UsersTable.query.all()  # Get all users from the database
    return render_template('index.html', users = users)'


# Route to add a user
@app.route('/add', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = UsersTable(user_name=name, email=email)
        try:
            SQLA.db.session.add(new_user)
            SQLA.db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return str(e)
    
    return render_template('add_user.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
'''