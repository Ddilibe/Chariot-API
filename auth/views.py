#!/usr/bin/env python3
""" Script for the views for auth blueprint """
import json
import base64
import logging
from . import auth
from cart.models import Cart
from .models import User, CreditCart
from flask.views import MethodView
from flask import request, jsonify, session
from run import db, login_manager, redis_cli
from utils.exception import NotAbleToBeAnAdminError
from flask_login import login_required, current_user
from .backend import authenticate, generate_token, valid_request, retrieve_user, logout_user
from utils.exception import UserNonExistError, PasswordNotCorrectError, InvalidUserAttributes


@auth.route("/login", strict_slashes=False, methods=["POST"])
def login():
    """
    Function for sigining into the database
    Args:
        No arguments
    Return:
        Return values depends the success and exist of the route
    """
    request_data, info, code = request.get_json(), {}, ''
    try:
        email, password = request_data.get("email_address"), request_data.get('password')
        if not (authenticate(email_address=email, password=password)):
            raise InvalidUserAttributes("Username and password cannot be authenticated")
        token = generate_token(email)
        info["Login"], code = "Successful", 200
        info["Message"] = f"User {email} has login in"
        if token:
            info.update(**token)
    except Exception as e:
        info["Login"], info['error code'] = "Unsuccessful", str(e)
        info["Message"] = f"User {email} cannot login in"
        info["error"], code = "Invalid Username or password", 401
    finally:
        return jsonify(info), code

@auth.route("/logout", strict_slashes=False, methods=["POST"])
@valid_request
def logout():
    """
    Function for signing out from the api
    Args:
        :params: user_id[str] - The id of a logged in user
    Return:
        For successful verification, it will sign the user out else
        it would reply with an error
    """
    info = {}
    if logout_user():
        code, info["Logout"] = 200, "Successful"
        info["Message"] = f"User has logged out"
    else:
        info["Logout"], code = "Logout is Unsuccessful", 403
        info['Message'] = str(e)
    return jsonify(info), code

@auth.route("/signup", strict_slashes=False, methods=["POST"])
def signup():
    """ Function for sigining up to the API
    or function for registering as a user in this api
    """
    request_data, info = request.get_json(), {}
    try:
        new_user, new_cart = User(**request_data), Cart()
        new_user.cart = new_cart
        logging.debug("Done")
        db.session.add(new_user)
        db.session.commit()
        info["Signup"], code = "Successful", 201
        info["Message"] = f"User {request_data.get('email_address')} has signed up"
    except Exception as e:
        info["Signup"] = "Failure"
        info["Message"] = "Invalid credential for signup"
        info["Error"], code = f"{e}", 400
    return jsonify(info), code

@auth.route("/check", strict_slashes=False, methods=["GET"])
@valid_request
def check():
    info = {"1": "one", "2": "two", "3": "three"}
    return jsonify(info)

@auth.route("/newsletter", strict_slashes=False, methods=["POST", "DELETE"])
@valid_request
def newletter_subscription():
    info, user, code = {}, retrieve_user(), 201
    if request.method == "POST":
        info["Newletter Subscription"] = user.subscribe_newletter()
    if request.method == "DELETE":
        info["Newletter Subscription"] = user.unsubscribe_newletter()
    return jsonify(info), code

@auth.route("/admin", strict_slashes=False, methods=["GET", "POST"])
@valid_request
def check_or_convert_admin(user_id):
    info, code = {}, 200
    try:
        user = retrieve_user()
        if request.method == "GET":
            info["admin"] = user.admin(), 200
        if request.method == "POST":
            info['admin'] = user.become_admin()
    except Exception as e:
        info["error"], code = str(e), 404
    finally:
        return jsonify(info), code

@auth.route('/merchant', strict_slashes=False, methods=['GET', 'PUT'])
@valid_request
def merchant_actions():
    """
        Function for making an active user to be a merchant
    """
    user, info = retrieve_user(), {}
    try:
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

@auth.route('/addcreditcard', strict_slashes=False, methods=['POST'])
@valid_request
def add_credit_card():
    info = {}
    try:
        user, request_data = retrieve_user(), request.get_json()
        user.create_credit_card(**request_data)
        info["credit"], code = "Successful", 200
    except Exception as e:
        info['Error'], code = str(e), 403
    return jsonify(info), code

class CreditCard(MethodView):

    methods = ['GET', "PUT", "DELETE"]
    decorators = [valid_request]
    model = CreditCart

    def get(self, name, *args, **kwargs):
        if card := CreditCard.query.filter_by(id):
            values = card.produce()
            return jsonify(values), 201
        return jsonify({"error": "Card identifier not valid"}), 404

    def put(self, name, *arg, **kwargs):
        if card := CreditCard.query.filter_by(id):
            values = card.update(request.get_json())
            return jsonify(values), 201
        return jsonify({"error": "Card could not update"})

    def delete(self, name, *args, **kwargs):
        if card := CreditCard.query.filter_by(id):
            if values := card.delete():
                return jsonify({"card": "Deleted Successfully"}), 200
        return jsonify({"error":"Card could not be deleted"})


auth.add_url_rule('/creditcard/<name>', view_func=CreditCard.as_view("credit_card"))
