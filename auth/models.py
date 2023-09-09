#!/usr/bin/env python3
""" Script for the models for the auth blueprint """
from werkzeug.security import generate_password_hash, check_password_hash
from utils.exception import NotAbleToBeAnAdminError
from flask_login import UserMixin
import enum, uuid, json, base64
from run import db
from . import auth
import stripe


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


class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(db.String(50), primary_key=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False, index=True)
    user_name = db.Column(db.String(255), nullable=False, index=True)
    profile_picture = db.Column(db.String(255), nullable=True, index=True)
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
    logged = db.Column(db.Boolean, default=False)
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
        pic = kwargs.get('profile_picture')
        pic_name = kwargs.get('picture_name')

    @property
    def password(self):
        raise AttributeError("Password is not a readable object")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_merchant(self):
        """ Function for creating a connected account for payment """
        connected_account = stripe.Account.create(
            type='standard',
            country=self.country,
            email=self.email_address
        )
        self.stripe_account = connected_account.id
        self.save()

    def become_merchant(self):
        """ Method for becomming a merchant """
        if not self.is_merchant:
            self.is_merchant = True
            self.merchant_id = str(uuid.uuid4())
            self.create_merchant()

    def admin(self):
        return self.is_admin

    def save(self):
        db.session.add(self)
        db.session.commit()

    def subscribe_newletter(self):
        if self.newletter_subscription == NewletterSubEnum.true:
            return "You have a Newsletter Subscription"
        self.newletter_subscription = NewletterSubEnum.true
        self.save()
        return "You just subscribed to the newsletter"

    def unsubscribe_newletter(self):
        if self.newletter_subscription == NewletterSubEnum.false:
            return "You don't have a newletter subscription"
        self.newletter_subscription = NewletterSubEnum.false
        self.save()
        return "You just unsubscribed to the newsletter"

    def create_credit_card(self, **kwargs):
        new_credit_card = CreditCart(
            id=str(uuid.uuid4()),
            number=kwargs['number'],
            exp_month=kwargs['exp_month'],
            exp_year=kwargs['exp_year'],
            user_id=self.id,
            cvc=kwargs['cvc']
        )
        db.session.add(new_credit_card)
        db.session.commit()

    def qualify_for_admin(self):
        if self.credit_card and self.newletter_subscription==NewletterSubEnum.true:
            return True
        return False

    def become_admin(self):
        if not self.is_admin:
            if not self.qualify_for_admin():
                words = "This user is not qualified to be an admin. "
                words += "Add at least one credit card and subscribe to our newsletter"
                return words
            self.is_admin = True
            self.save()
        return "User is successfully an admin"

class CreditCart(db.Model):
    """
        Class for Model repersentation of the credit table database

        Variable description
        @args: __tablename__[str] - Name of the table in database
        @args: Id[uuid(str)] - unique id to repersent the credit card
        @args: number[int] - The number in the credit card
        @args: exp_month[int] - The month the credit card is expiring
        @args: exp_year[int] - The year the credit card is expiring
        @args: cvc[int] - The cvc of the credit card
        @args: user_id[int] - A foreign key relationship to the user
    """
    __tablename__ = "credit_card"

    object_type = "card"
    id = db.Column(db.String(50), primary_key=True, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    exp_month = db.Column(db.Integer, nullable=False)
    exp_year = db.Column(db.Integer, nullable=False)
    cvc = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """ Method for initiating the class """
        super(CreditCart, self).__init__(*args, **kwargs)

    def produce(self):
        return {
            "object": self.object_type,
            "number": self.number, "exp_year": self.exp_year,
            "exp_month": self.exp_month
        }
    def all(self):
        return {
            "object": self.object_type,
            "number": self.number, "exp_year": self.exp_year,
            "exp_month": self.exp_month, "cvc":self.cvc
        }

    def update(self, request):
        names, info = ['number', 'exp_month', 'exp_year', 'cvc'],{}
        info['values'] = []
        for keys, values in request.items():
            if key in names:
                if value != self.all.get(value):
                    info["values"].append(key)
                    self.set(key, value)
        self.save()
        info["update"] = "successful"
        return info

    def delete(self):
        db.session.delete(self)
        db.session.commit()



