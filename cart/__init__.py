#!/usr/bin/env python3
""" Script for the blueprint for the cart """
from flask import Blueprint


cart = Blueprint('cart', __name__)


from . import models, errors, views
