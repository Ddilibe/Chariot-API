#!/usr/bin/env python3
""" Script for the docs section of the product """
from flask import Blueprint

docs = Blueprint('docs', __name__)

from . import views
