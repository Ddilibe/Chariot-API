#!/usr/bin/env python3
""" Script to handle the error for the auth blueprint """
from . import auth
from flask import jsonify


@auth.app_errorhandler(404)
def page_not_found(e):
    info = {
        "Error": "Page doesn't exist"
    }
    return jsonify(info)
