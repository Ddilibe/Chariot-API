#!/usr/bin/env python3
""" Script for initializing the auth folder with flask blueprint """
from flask import Blueprint


auth = Blueprint('auth', __name__)


from . import error, views, models
