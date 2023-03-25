#!/usr/bin/env python3
""" Script for the views for auth blueprint """
import json
import base64
import logging
from . import auth
from cart.models import Cart
from .models import User, UserPicture
from sqlalchemy_media import StoreManager
from flask import request, jsonify, session
from run import db, login_manager, redis_cli
from utils.decorators import user_has_loggedin
from flask_login import logout_user, login_user
from utils.exception import NotAbleToBeAnAdminError
from flask_login import login_required, current_user
from utils.exception import UserNonExistError, PasswordNotCorrectError


@auth.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    """
    Function for sigining into the database
    Args:
        No arguments
    Return:
        Return values depends the success and exist of the route
    """
    info = {}
    try:
        logging.debug("Using request to obtain the data passed")
        request_data = request.get_json()
        email = request_data.get("email_address")
        password, info["error"] = request_data.get("password"), {}
        logging.info("Gotten the email and password data")
        user = User.query.filter_by(email_address=email).first_or_404()
        word = user.verify_password(password)
        if not word:
            ans = f"Password entered by user {email} is not correct"
            info["error"]["Incorrect Password"] = ans
            raise PasswordNotCorrectError
        name = user.user_name
        avg = redis_cli.get(name)
        if avg:
            key = avg.decode("utf-8")
            info["Twice"] = "You have logged in before"
        else:
            key = redis_cli.store(email)
            redis_cli.session(name, key)
        db.session.add(user)
        db.session.commit()
        logging.info("Trying to login")
        w = login_user(user, remember=True)
        logging.info(f"Done logging {w}")
        info["Login"], code = "Successful", 200
        info["Key"], info["Message"] = key, f"User {email} has login in"
    except Exception as e:
        info["Login"] = "Unsuccessful"
        info["Message"] = f"User {email} cannot login in"
        info["error"]["Invalid Enteries"], code = "Invalid Username or password", 401
    finally:
        return jsonify(info), code


@user_has_loggedin
@auth.route("/logout/<user_id>", strict_slashes=False, methods=["POST", "GET"])
def logout(user_id):
    """
    Function for signing out from the api
    Args:
        :params: user_id[str] - The id of a logged in user
    Return:
        For successful verification, it will sign the user out else
        it would reply with an error
    """
    info = {}
    logging.info("Creating the info dict")
    try:
        logging.debug(f"The username is")
        user = user_has_loggedin(user_id)
        redis_cli.dele(user.user_name)
        logging.debug(f"They have gotten the user")
        redis_cli.dele(user_id)
        db.session.add(user)
        db.session.commit()
        logging.debug(f"Starting to logout")
        logout_user()
        logging.debug(f"Done logging out {user.email_address}")
        code, info["Logout"] = 200, "Successful"
        info["Message"] = f"User {user.email_address} has logged out"
    except Exception as e:
        info["Logout"], code = "Logout is Unsuccessful", 403
        info['Message'] = json.loads(e)
        logging.info("An error occured")
    finally:
        return jsonify(info), code


@auth.route("/signup", strict_slashes=False, methods=["GET", "POST"])
def signup():
    """ Function for sigining up to the API
    or function for registering as a user in this api
    """
    info = {}
    try:
        logging.info("Starting the signingup of a new user")
        with StoreManager(db.session):
            logging.info("Starting the signingup of a new user Step 1")
            logging.info("Getting the request in json format")
            request_data = request.get_json()
            logging.debug(f"Confirming the type of request_data {type(request_data)}")
            new_user, new_cart = User(**request_data), Cart()
            logging.info(
                """ User attribute has accepted email_address
                    User attribute has accepted username
                    User attribute has accepted first_name
                    User attribute has accepted last_name
                    User attribute has accepted phone_number
                    User attribute has accepted gender """
            )
            new_user.cart = new_cart
            db.session.add(new_user)
            db.session.commit()
            wants1 = ["email_address", "user_name", "first_name"]
            wants2 = ["last_name", "phone_number", "gender"]
            wants = wants1 + wants2
            for value in wants:
                info[value] = request_data.get(value)
                logging.info(f"Added {value} to the info dict")
            info["Signup"], code = "Successful", 201
            info["Message"] = f"User {info['email_address']} has signed up"
    except Exception as e:
        info["Signup"] = "Failure"
        info["Message"] = "Invalid credential for signup"
        info["Error"], code = f"{e}", 400
    return jsonify(info), code


@auth.route("/check", strict_slashes=False, methods=["GET"])
@login_required
def check():
    info = {"1": "one", "2": "two", "3": "three"}
    return jsonify(info)


@auth.route("/<user_id>/newsletter", strict_slashes=False, methods=["POST", "DELETE"])
def newletter_subscription(user_id):
    info = {}
    info["error"] = {}
    try:
        user = user_has_loggedin(user_id)
        if request.method == "POST":
            if not user.newletter_subscription:
                user.newletter_subscription = "true"
                info["Newletter Subscription"] = "You have subscribed to the newsletter"
            else:
                info["Newletter Subscription"] = "You already have a subscription"
        if request.method == "DELETE":
            if user.newletter_subscription:
                user.newletter_subscription = "False"
                info["Newletter Subscription"] = "You have removed subscription "
                info["Newletter Subscription"] += "to the newsletter"
            else:
                info["Newletter Subscription"] = "You don't have a subscription"
        info["login"], info["error"], info["Complete Sub"] = True, None, "Successful"
    except Exception as e:
        info['Message'] = json.loads(e)
    finally:
        return jsonify(info), 201


@auth.route("/<user_id>/verify", strict_slashes=False, methods=["GET", "POST"])
def verify_user(user_id):
    pass


@auth.route("/<user_id>/admin", strict_slashes=False, methods=["GET", "POST", "PUT"])
def check_or_convert_admin(user_id):
    try:
        info = {}
        user, info['error'] = user_has_loggedin(user_id), {}
        if request.method == "GET":
            info["admin"], code = user.is_Admin(), 200
        if request.method == "PUT":
            logging.debug("Started Put Method")
            for keys in user.__dict__:
                if user.__dict__.get(keys) == None:
                    logging.debug(f"Ended Put Method {user.__dict__.get(keys)}")
                    words = "This user is not qualified to be an admin"
                    words += "Complete your profile before you apply for admin"
                    info["error"]["No User"] = words
                    logging.debug(f"Debugging error {words}")
                    raise NotAbleToBeAnAdminError(words)
                logging.debug("Ended Put Method")
            user.is_admin = True
            info["admin"], info["admin text"] = (
                True,
                "You have been granted admin priviledges",
            )
            db.session.commit()
    except NotAbleToBeAnAdminError as e:
        # info["error"]["No User"] = e
        pass
    finally:
        return jsonify(info), 200

def user_has_loggedin(user_id):
    logging.info("Testing the decorated function")
    email = redis_cli.get(user_id)
    if not email:
        raise UserNotLoggedIn("User Has Not LoginIn")
    email = email.decode("utf-8")
    user = User.query.filter_by(email_address=email).first_or_404()
    return user

@auth.route('/<user_id>/merchant', strict_slashes=False, methods=['GET', 'PUT'])
def merchant_actions(user_id):
    """
        Function for making an active user to be a merchant
    """
    try:
        user, info = user_has_loggedin(user_id), {'id': user_id}
        if request.method == "GET":
            info['Merchant'] = user.is_merchant
        if request.method == "PUT":
            user.become_merchant()
            db.session.commit()
            info['Merchant'] = user.is_merchant
        code = 201
    except Exception as e:
        info['error'], code = e, 403
    finally:
        return jsonify(info), code
