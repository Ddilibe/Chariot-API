#!/usr/bin/env python3
from flask import Blueprint


prod = Blueprint("prod", __name__)


from . import views, models
