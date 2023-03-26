#!/usr/bin/env python3
""" Script for the view for the cart blueprint """
import stripe
import logging
import functools
from . import cart
from .models import Cart
from auth.models import User
from run import db, redis_cli
from prod.models import Product
from utils.exception import UserNotLoggedIn
from flask import request, jsonify, redirect


@cart.route("/<user_id>/all", strict_slashes=False, methods=["GET"])
def display_cart(user_id):
    """Function for displaying what is in a cart"""
    info = {}
    info["error"] = {}
    try:
        request_data = request.get_json()
        user = user_has_loggedin(user_id)
        cart, code = user.cart.display_item(), 200
    except Exception as e:
        info["error"]["Error Occured"] = "Cart inexistent for such User"
        code = 403
    finally:
        return jsonify(info)


@cart.route("/act/<user_id>", strict_slashes=False, methods=["DELETE", "POST"])
def action_cart(user_id):
    """Function for performing a delete or post function in the
    in the cart"""
    info = {}
    info["error"] = {}
    try:
        user = user_has_loggedin(user_id)
        if request.method == "POST":
            user.cart.items.add_item(request_data["add_to_cart"])
        if request.method == "DELETE":
            cart_item = user.cart.items.get_item(
                request_data["remove_from_cart"]
            )
            user.cart.remove_item(cart_item)
        code = 203
    except Exception as e:
        info["error"]["Error Occured"] = "Cart inexistent for such User"
        code = 401
    finally:
        return jsonify(info), code


@cart.route("/failure", strict_slashes=False, methods=["GET"])
def cart_failure():
    """Function for a failure during the checkout process"""
    info = {"Payment": "Failure"}
    return jsonify(info), 401


@cart.route("/<user_id>/checkout", methods=["POST"])
def create_checkout_session(user_id):
    try:
        user, line_items, info = user_has_loggedin(user_id), [], {}
        for item in user.cart.items:
            prod = Product.query.filter_by(
                prod_id=item.product_id
            ).first_or_404()
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": prod.name},
                        "unit_amount": int(prod.price),
                    },
                    "quantity": item.quantity,
                }
            )
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:5000/cart/succesful",
            cancel_url="http://localhost:5000/cart/failure",
        )
        info["sessionId"] = checkout_session["id"]
    except Exception as e:
        info["error"] = e
    finally:
        return redirect(checkout_session.url, param=jsonify(info))


@cart.route("/succesful", strict_slashes=False, methods=["GET"])
def success():
    """Function for indicating a successful transaction"""
    session_id = request.args.get("session_id")
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    order = {
        "customer_email": checkout_session["customer_details"]["email"],
        "shipping_address": checkout_session["shipping"]["address"],
        "items": [],
        "total_amount": checkout_session["amount_total"] / 100,
    }
    for item in checkout_session["display_items"]:
        order["items"].append(
            {
                "name": item["custom"]["name"],
                "quantity": item["quantity"],
                "price": item["amount"] / 100,
            }
        )
    # Save order to database
    # ...
    return jsonify({"Order": "Order successful"}), 200


def user_has_loggedin(user_id):
    """Function for obtaining a user who login in"""
    logging.info("Testing the decorated function")
    email = redis_cli.get(user_id)
    if not email:
        raise UserNotLoggedIn("User Has Not LoginIn")
    email = email.decode("utf-8")
    user = User.query.filter_by(email_address=email).first_or_404()
    return user
