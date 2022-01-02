from flask_sqlalchemy import SQLAlchemy
from com import app, BCRYPT, login_manager
from flask_login import UserMixin

DB = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return UsersDB.query.get(int(user_id))

class UsersDB(DB.Model, UserMixin):
    id = DB.Column(DB.Integer(), primary_key=True)
    username = DB.Column(DB.String(length=30), nullable=False, unique=True)
    email = DB.Column(DB.String(length=30), nullable=False, unique=True)
    password_enc = DB.Column(DB.String(length=68), nullable=False)
    budget = DB.Column(DB.Integer(), nullable=False, default=1000)
    items = DB.relationship('ItemsDB', backref='owned_user', lazy=True)

    @property
    def string_budget(self):
        if(len(str(self.budget)) >= 4):
            return "${:,.2f}".format(self.budget)
        else:
            return f"${self.budget}"

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, password_text):
        self.password_enc = BCRYPT.generate_password_hash(password_text).decode('utf-8')
    
    def check_password(self, attempted_password):
        return BCRYPT.check_password_hash(self.password_enc, attempted_password)
    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

class ItemsDB(DB.Model):
    id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(length=20), nullable=False, unique=True)
    price = DB.Column(DB.Integer(), nullable=False)
    barcode = DB.Column(DB.String(length=12), nullable=False, unique=True)
    description = DB.Column(DB.String(length=50), nullable=True, unique=True)
    owner = DB.Column(DB.Integer(), DB.ForeignKey('usersDB.id'), nullable=True)

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        DB.session.commit()