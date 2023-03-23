#!/usr/bin/env python3
""" Script for the view for the cart blueprint """
from . import cart
from .models import Cart
from auth.models import User
from run import db, redis_cli
from flask import request, jsonify


@cart.route('/all', strict_slashes=False, methods=['GET'])
def display_cart():
    info = {}
    info['error'] = {}
    try:
        request_data = request.get_json()
        user_id = request_data.get(user_name)
        email = (redis_cli.get(user_id)).decode('utf-8')
        if email:
            info['Login'] = True
            logging.debug(f"The username is {email}")
            user = User.query.filter_by(email_address=email).first()
            if user:
                cart = user.cart.display_item()
                info['cart'] = cart
            else:
                info['error']['Invalid User'] = "User doesn't not exists"
        else:
            info['error']['Login'] = "Invalid Login session"
            info['Login'] = False
    except Exception as e:
        info['error']['Error Occured'] = "Cart inexistent for such User"
    finally:
        return jsonify(info)


@cart.route('/act/<prod_id>', strict_slashes=False, methods=['DELETE', "POST"])
def action_cart(prod_id):
    info = {}
    info['error'] = {}
    if request.method == "POST":
        try:
            request_data = request.get_json()
            user_id = request_data.get(user_name)
            email = (redis_cli.get(user_id)).decode('utf-8')
            if email:
                info['Login'] = True
                user = User.query.filter_by(email_address=email).first()
                if user:
                    user.cart.products.add_item(request_data['add_to_cart'])
                    db.session.commit()
                else:
                    info['error']['Invalid User'] = "User doesn't not exists"
            else:
                info['error']['Login'] = "Invalid Login session"
                info['Login'] = False
        except Exception as e:
            info['error']['Error Occured'] = "Cart inexistent for such User"
        finally:
            return jsonify(info)
    if request.method == "DELETE":
        try:
            request_data = request.get_json()
            user_id = request_data.get(user_name)
            email = (redis_cli.get(user_id)).decode('utf-8')
            if email:
                info['Login'] = True
                user = User.query.filter_by(email_address=email).first()
                if user:
                    cart_item = user.cart.products.get_item(request_data['remove_from_cart'])
                    user.cart.products.remove_item(cart_item)
                    db.session.commit()
                else:
                    info['error']['Invalid User'] = "User doesn't not exists"
            else:
                info['error']['Login'] = "Invalid Login session"
                info['Login'] = False
        except Exception as e:
            info['error']['Error Occured'] = "Cart inexistent for such User"
        finally:
            return jsonify(info)

@cart.route('/succesful', strict_slashes=False, methods=['GET'])
def cart_successful():
    """ Function for a successful purchase of product """
    info = {
        "Payment": "Successful",
    }
    return jsonify(info), 200

@cart.route('/failure', strict_slashes=False, methods=['GET'])
def cart_failure():
    """ Function for a failure during the checkout process """
    info = {
        "Payment": "Failure"
    }
    return jsonify(info), 401
