#!/usr/bin/env python3
""" Script for the blueprint for the cart """
from flask import blueprint


cart = blueprint('cart', __name__)


from . import models, error, views
