#!/usr/bin/env python3
""" Script for the models for the auth blueprint """
from run import db
from . import auth
import enum, uuid, json, base64
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_media import Image, ImageAnalyzer, ImageValidator, ImageProcessor


class UserPicture(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(80, 80),
            maximum=(800, 600),
            content_types=['image/jpeg', 'image/png']
        ),
        ImageProcessor(
            fmt='jpeg',
            width=120,
        )
    ]


class Json(db.TypeDecorator):
    impl = db.Unicode

    def process_bind_param(self, value, engine):
        return json.dumps(value)

    def process_result_value(self, value, engine):
        return json.loads(value) if value else None


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
    profile_picture = db.Column(UserPicture.as_mutable(Json))
    last_name = db.Column(db.String(255), nullable=False, index=True)
    email_address = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.dwti, nullable=False)
    newletter_subscription = db.Column(db.Enum(NewletterSubEnum),
        default=NewletterSubEnum.false, nullable=False)
    account_status = db.Column(db.Enum(AccountStatEnum),
        default=AccountStatEnum.not_ver, nullable=False)
    merchant_id = db.Column(db.String(128))
    cart = db.relationship("Cart", uselist=False, back_populates='user')
    is_admin = db.Column(db.Boolean(), default=False)
    # billing_address =
    # shipping_address =
    # payment_info =
    # order_history =
    # wishlist =
    # review =

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())
        self.merchant_id = str(uuid.uuid4())
        self.password_hash = generate_password_hash(kwargs.get('password'))
        pic = kwargs.get('profile_picture')
        pic_name = kwargs.get('picture_name')
        if pic and pic_name:
            pic = bytes(pic, 'utf-8')
            with open(pic_name, 'wb') as pic_file:
                pic_file.write(base64.b64decode((pic)))
            user.profile_picture = UserPicture.create_from(pic_name)

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
