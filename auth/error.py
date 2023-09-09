#!/usr/bin/env python3
""" Script to handle the error for the auth blueprint """
from . import auth
from flask import jsonify


@auth.app_errorhandler(404)
def page_not_found(e):
    info = {
        "Error": str(e)
    }
    return jsonify(info)

@auth.app_errorhandler(415)
def unsupported_media_type(e):
    info = {'error': e}
    return jsonify(info), 415
""" Error
        405: Method not allowed
        406: if it not json, it is not acceptable
        415: Unsupported Media type
        204: Successfully processed but no content returned
        401: Not authorized
        400: Bad request
        403: Forbidded request
        404: Not found request
"""
