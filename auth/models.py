#!/usr/bin/env python3
""" Script for the models for the auth blueprint """
import stripe
from run import db
from . import auth
from dotenv import load_dotenv
import enum, uuid, base64, re, os
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

load_dotenv()

class GenderEnum(enum.Enum):
    male = "MALE"
    female = "FEMAlE"
    dwti = "Don't Want to identify"

class NewletterSubEnum(enum.Enum):
    true = True
    false = False

class AccountStatEnum(enum.Enum):
    veri = "Verified"
    not_ver = "Not Verified"

from sqlalchemy import Column
Column()

class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(db.String(50), primary_key=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False, index=True)
    user_name = db.Column(db.String(255), nullable=False, index=True)
    profile_picture = db.Column(db.String(255))
    last_name = db.Column(db.String(255), nullable=False, index=True)
    email_address = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.dwti, nullable=False)
    newletter_subscription = db.Column(db.Enum(NewletterSubEnum),
        default=NewletterSubEnum.false, nullable=False)
    account_status = db.Column(db.Enum(AccountStatEnum),
        default=AccountStatEnum.not_ver, nullable=False)
    is_merchant = db.Column(db.Boolean(), default=False)
    merchant_id = db.Column(db.String(128))
    cart = db.relationship("Cart", uselist=False, back_populates='user')
    is_admin = db.Column(db.Boolean(), default=False)
    currency = db.Column(db.String(22), default="usd")
    stripe_account = db.Column(db.String(128))
    credit_card = db.relationship('CreditCart', backref='User', lazy=True)
    # billing_address =
    # shipping_address =
    # payment_info =
    # order_history =
    # wishlist =
    # review =

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if kwargs.get('is_merchant'):
            self.merchant_id = str(uuid.uuid4())
            self.create_merchant()
        self.id = str(uuid.uuid4())
        self.password_hash = generate_password_hash(kwargs.get('password'))
    
        
    @validates("profile_picture")
    def validates_user_profile_picture(self, key, value):
        media = os.environ['MEDIASTORAGE']
        if not re.fullmatch(r"{{media}}/{{self.user_name}}/\w+.jpeg", value):
            return value
        raise ValueError("Path for storing image does not match")

    @property
    def password(self):
        raise AttributeError("Password is not a readable object")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_Admin(self):
        return self.is_admin

    def create_merchant(self):
        """ Function for creating a connected account for payment """
        connected_account = stripe.Account.create(
            type='standard',
            country=self.country,
            email=self.email_address
        )
        self.stripe_account = connected_account.id
        db.session.add(self)
        db.session.commit()

    def become_merchant(self):
        """ Method for becomming a merchant """
        if not self.is_merchant:
            self.is_merchant = True
            self.merchant_id = str(uuid.uuid4())
            self.create_merchant()


class CreditCart(db.Model):
    __tablename__ = "credit_card"

    object_type = "card"
    id = db.Column(db.String(50), primary_key=True, nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    exp_month = db.Column(db.Integer, nullable=False)
    exp_year = db.Column(db.Integer, nullable=False)
    cvc = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(CreditCart, self).__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())
    
    @validates('exp_year')
    def verify_exp_year(self, val, key):
        start_date = datetime.now().year
        if key not in range(start_date-4, start_date+4):
            raise ArithmeticError
        return key
        
    @validates('exp_month')
    def verify_exp_month(self, val, key):
        if key not in range(1, 13):
            raise ArithmeticError
        return key
    
    @validates('exp_cvc')
    def verify_cvc(self, val, key):
        if key not in range(1, 1000):
            raise ArithmeticError
        return key

    def produce(self):
        return {
            "object": self.object_type,
            "number": self.number, "exp_year": self.exp_year,
            "exp_month": self.exp_month, "cvc": self.cvc
        }
