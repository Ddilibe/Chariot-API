#!/usr/bin/env python3
""" Script for the views for auth blueprint """
import logging
from . import auth
from run import db, login_manager
from .models import User, UserPicture
from sqlalchemy_media import StoreManager
from flask import request, jsonify, session
from flask_login import login_required, login_user, current_user


@auth.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    request_data = request.get_json()
    logging.debug("Using request to obtain the data passed")
    email = request_data.get('email_address')
    password = request_data.get('password')
    logging.info("Gotten the email and password data")
    user = User.query.filter_by(email_address=email).first()
    if user:
        if word := user.verify_password(password):
            session[email]  = user.user_name
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return jsonify({
                    "Login": "Successful",
                    "Message": f"User {email} has login in"
                }), 200
    return jsonify({
            "Login": "Unsuccessful",
            "Message": f"User {email} has login in",
            "Error": "Invalid Username or password"
        }), 401


@auth.route('/logout/<user_id>', strict_slashes=False, methods=['POST', 'GET'])
def logout(user_id):
    # request_data = request.get_json()
    # user = current_user.email_address
    # if session.get(email):
    # if current_user.is_authenticated:
    new_id = [i for i, j in session.items() if j == user_id][0]
    user = User.query.filter_by(email_address=new_id)
    if user.is_authenticated:
        user.authenticated = False
    db.session.add(user)
    db.session.commit()
    del session[email]
    logout_user()
    return jsonify({
            "Logout": "Successful",
            "Message": f"User {email} has logged out"
        })


@auth.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def signup():
    try:
        logging.info("Starting the signingup of a new user")
        with StoreManager(db.session):
            logging.info("Starting the signingup of a new user Step 1")
            user = User()
            logging.info("Getting the request in json format")
            request_data = request.get_json()
            logging.debug(f"Confirming the type of request_data {type(request_data)}")
            user.email_address = request_data.get('email_address')
            logging.info("User attribute has accepted email_address")
            user.user_name = request_data.get('user_name')
            logging.info("User attribute has accepted username")
            user.first_name = request_data.get("first_name")
            logging.info("User attribute has accepted first_name")
            user.last_name = request_data.get("last_name")
            logging.info("User attribute has accepted last_name")
            user.phone_number = request_data.get("phone_number")
            logging.info("User attribute has accepted phone_number")
            user.gender = request_data.get("gender")
            logging.info("User attribute has accepted gender")
            if pic := request_data.get('profile_picture'):
                user.profile_picture = UserPicture.create_from(pic)
            user.password = request_data.get('password')
            db.session.add(user)
            db.session.commit()
            e = request_data.get('email_address')
            return jsonify({
                    "Signup": "Successful",
                    "Message": f"User {e} has signed up",
                    "email_address": request_data.get('email_address'),
                    "user_name": request_data.get('username'),
                    "first_name": request_data.get("first_name"),
                    "last_name": request_data.get("last_name"),
                    "phone_number": request_data.get("phone_number"),
                    "gender": request_data.get("gender")
                }), 200
    except Exception as e:
        return jsonify({
                "Signup" : "Failure",
                "Message": "Invalid credential for signup",
                "Error": f"{e}"
            }), 400


@auth.route('/check/<user_id>', strict_slashes=False, methods=['POST', "GET"])
@login_required
def check_for_login(user_id):
    return jsonify({
            "Name": dir(current_user),
        })
