from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='user')

    def __repr__(self):
        return f'<User {self.username}>'

# Categories model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    expiry_date = db.Column(db.Date)
    manufacture_date = db.Column(db.Date)
    price = db.Column(db.Float)
    unit = db.Column(db.String())
    quantity = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sold_quantity = db.Column(db.Float)

    def __repr__(self):
        return f'<Product {self.name}>'

# Create all tables
with app.app_context():
    db.create_all()

    # Check if admin user exists
    if User.query.filter_by(username='admin').first() is None:
        admin_password = generate_password_hash('adminpassword')

        admin = User(username='admin', email='admin@grocery.com', password=admin_password, role='admin')
        db.session.add(admin)
        db.session.commit()
    else:
        print('Admin already exists')

    # Check if categories exist
    if Category.query.count() == 0:
        # Create Categories
        fruits = Category(name='Fruits')
        vegetables = Category(name='Vegetables')
        dairy = Category(name='Dairy')

        db.session.add_all([fruits, vegetables, dairy])
        db.session.commit()
    else:
        print('Categories already exist')

    # Check if products exist
    if Product.query.count() == 0:
        # Create Products
        apple = Product(name='Apple', category_id=1, price=1.99, unit='kg', quantity=100, expiry_date=datetime(2024, 12, 31), manufacture_date=datetime(2024, 6, 1), created_user_id=1)
        banana = Product(name='Banana', category_id=1, price=0.99, unit='bunch', quantity=50, expiry_date=datetime(2024, 12, 31), manufacture_date=datetime(2024, 6, 1), created_user_id=1)
        potato = Product(name='Potato', category_id=2, price=0.49, unit='kg', quantity=200, expiry_date=datetime(2024, 12, 31), manufacture_date=datetime(2024, 6, 1), created_user_id=1)
        milk = Product(name='Milk', category_id=3, price=2.49, unit='liter', quantity=20, expiry_date=datetime(2024, 6, 30), manufacture_date=datetime(2024, 6, 1), created_user_id=1)

        db.session.add_all([apple, banana, potato, milk])
        db.session.commit()
    else:
        print('Products already exist')


