#!/usr/bin/env python3
""" Script for running the whole operation on chariot """
from sqlalchemy_media import StoreManager, FileSystemStore
# from auth.models import User, UserPicture
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from utils.rediscli import Cache
from flask import Flask, session
from flask_moment import Moment
from datetime import timedelta
from flask_mail import Mail
from flasgger import Swagger
from config import config
import functools
import logging
import stripe
import click
import os

env = os.getenv('FLASK_CONFIG')
config_name = ( env if env else 'default').lower()


login_manager, redis_cli = LoginManager(), Cache()
mail, moment, db = Mail(), Moment(), SQLAlchemy()
WORKING_DIR = os.path.abspath(os.getcwd())
TEMP_PATH = os.path.join(WORKING_DIR, 'static', 'avatars')

app = Flask(__name__)

app.logger.info("Starting app")
app.config.from_object(config[config_name])
config[config_name].init_app(app)
login_manager.login_view = 'auth.login'

app.logger.info(" Initializing App for mail, moment, db and login_manager")
mail.init_app(app)
moment.init_app(app)
db.init_app(app)
login_manager.init_app(app)

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY') or "sk_test_51MphMeBlSX2qNNEzNZLabtJiTddbkYLDFcYMh6cobTeiVOVXHWGNnnW9mfByCWNhMogPyDXvaK4KdxoMfxGEQTrD00CuwKgwom"
app.logger.info('Setting up the payment platform')
migrate = Migrate(app, db)
swagger = Swagger(app)

from auth import auth as auth_blueprint
from prod import prod as prod_blueprint
from cart import cart as cart_blueprint

app.logger.info("Initializing the blueprint")
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(prod_blueprint, url_prefix='/p')
app.register_blueprint(cart_blueprint, url_prefix='/cart')
with app.app_context():
    db.create_all()
app.logger.info("App Initializing done")




@app.shell_context_processor
def make_shell_context():
    dict_params = {
        # "User": User,
        # "UserPicture": UserPicture
    }
    return dict_params

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@login_manager.user_loader
def load_user(user_id):
    from auth.models import User
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.cli.command(help="Run the tests for the app.")
def tests():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
