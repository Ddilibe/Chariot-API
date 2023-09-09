#!/usr/bin/env python
""" script for authentication """
from dotenv import load_dotenv
from run import db, redis_cli
from functools import wraps
from config import config
from flask import request
from .models import User
import datetime
import jwt
import os

load_dotenv()

def generate_token(email_address):
    from .signals import token_about_to_expire
    from run import app
    user = db.session.query(User).filter(User.email_address==email_address).first_or_404()
    expiration_time = datetime.datetime.utcnow()+datetime.timedelta(minutes=1)
    token = jwt.encode({'user_id': user.id, 'exp': expiration_time}, app.config['SECRET_KEY'], algorithm='HS256')
    expiration_time = datetime.datetime.utcnow()+datetime.timedelta(seconds=55)
    token_about_to_expire.send(None, token=token, expiration_time=expiration_time)
    return {"Authorization": f"Chariot {token}"}


def verify_token(token):
    from run import app
    try:
        decoded_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        # Check if the token has expired
        if 'exp' in decoded_data and datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(decoded_data['exp']):
            raise jwt.ExpiredSignatureError
        else:
            return decoded_data['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def authenticate(email_address=None, password=None):
    if email_address and password:
        if user := db.session.query(User).filter(User.email_address==email_address).one_or_none():
            if confirm := user.verify_password(password):
                user.logged=True
                user.save()
                return True
    return False


def valid_request(value):
    @wraps(value)
    def check_token(*args, **kwargs):
        res = {'failure': "Authorization Failed"}
        if not ('Authorization' in request.headers.keys()):
            res['info'] = "Header attribute not found"
            return res
        author = request.headers.get('Authorization')
        if len(author.split()) != 2:
            res['info'] = "Token not present"
            return res
        name, token = author.split()
        if name != "Chariot":
            res['info'] = "Attribute before token not present"
            return res
        if not (user_id := verify_token(token)):
            res['info'] = "Token has expired or is non-existent"
            return res
        return value(*args, **kwargs)
    return check_token


def retrieve_user():
    author = request.headers.get('Authorization')
    name, token = author.split()
    user_id = verify_token(token)
    user = User.query.get(user_id)
    return user

def logout_user():
    from run import app
    user = retrieve_user()
    if not user:
        return False
    user.logged = False
    user.save()
    return True
