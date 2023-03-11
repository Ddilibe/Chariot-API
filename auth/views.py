#!/usr/bin/env python3
""" Script for the views for auth blueprint """
import base64
import logging
from . import auth
from .models import User, UserPicture
from sqlalchemy_media import StoreManager
from flask import request, jsonify, session
from run import db, login_manager, redis_cli
from flask_login import logout_user, login_user
from flask_login import login_required, current_user


@auth.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    request_data, info = request.get_json(), {}
    logging.debug("Using request to obtain the data passed")
    email = request_data.get('email_address')
    password = request_data.get('password')
    logging.info("Gotten the email and password data")
    if user := User.query.filter_by(email_address=email).first():
        if word := user.verify_password(password):
            name = user.user_name
            if avg := redis_cli.get(name):
                key = avg.decode('utf-8')
                info['Twice'] = "You have logged in before"
            else:
                key = redis_cli.store(email)
                redis_cli.session(name, key)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            info["Login"] =  "Successful"
            info["Key"] = key
            info["Message"], code = f"User {email} has login in", 200
    else:
        info["Login"] = "Unsuccessful"
        info["Message"] = f"User {email} cannot login in"
        info["Error"], code = "Invalid Username or password", 401
    return jsonify(info), code


@auth.route('/logout/<user_id>', strict_slashes=False, methods=['POST', 'GET'])
def logout(user_id):
    info = {}
    if email := (redis_cli.get(user_id)).decode('utf-8'):
        logging.debug(f"The username is {email}")
        user = User.query.filter_by(email_address=email).first()
        logging.debug(dir(user))
        redis_cli.dele(user_id)
        db.session.add(user)
        db.session.commit()
        logout_user()
        info["Logout"] = "Successful",
        info["Message"] = f"User {email} has logged out"
    else:
        info['Logout'] = "Logout is Unsuccessful"
        info['Message'] = "User is not logged at the moment"
    return jsonify(info)


@auth.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def signup():
    info = {}
    try:
        logging.info("Starting the signingup of a new user")
        with StoreManager(db.session):
            logging.info("Starting the signingup of a new user Step 1")
            user = User()
            logging.info("Getting the request in json format")
            request_data = request.get_json()
            logging.debug(f"Confirming the type of request_data {type(request_data)}")
            user.email_address = request_data.get('email_address')
            user.user_name = request_data.get('user_name')
            user.first_name = request_data.get("first_name")
            user.last_name = request_data.get("last_name")
            user.phone_number = request_data.get("phone_number")
            user.gender = request_data.get("gender")
            logging.info(""" User attribute has accepted email_address
                    User attribute has accepted username
                    User attribute has accepted first_name
                    User attribute has accepted last_name
                    User attribute has accepted phone_number
                    User attribute has accepted gender """)
            if pic := request_data.get('profile_picture'):
                pic_name = request_data.get('picture_name')
                pic = bytes(pic, 'utf-8')
                with open(pic_name, 'wb') as pic_file:
                    pic_file.write(base64.b64decode((pic)))
                user.profile_picture = UserPicture.create_from(pic_name)
            user.password = request_data.get('password')
            db.session.add(user)
            db.session.commit()
            e = request_data.get('email_address')
            info["Signup"] = "Successful"
            info["Message"] = f"User {e} has signed up",
            info["email_address"] = request_data.get('email_address'),
            info["user_name"] = request_data.get('user_name'),
            info["first_name"] = request_data.get("first_name"),
            info["last_name"] = request_data.get("last_name"),
            info["phone_number"] = request_data.get("phone_number"),
            info["gender"], code = request_data.get("gender"), 200
    except Exception as e:
        info["Signup"] = "Failure",
        info["Message"] = "Invalid credential for signup",
        info["Error"], code = f"{e}", 400
    return jsonify(info), code


@auth.route('/check', strict_slashes=False, methods=['GET'])
@login_required
def check():
    info = {
        "1": "one", "2": "two", "3": "three"
    }
    return jsonify(info)
