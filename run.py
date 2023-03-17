#!/usr/bin/env python3
""" Script for running the whole operation on chariot """
from config import config
from flask_mail import Mail
from datetime import timedelta
from flask_moment import Moment
from flask import Flask, session
from utils.rediscli import Cache
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from auth.models import User, UserPicture
from sqlalchemy_media import StoreManager, FileSystemStore
import functools
import logging
import os


mail, moment, db = Mail(), Moment(), SQLAlchemy()
login_manager, redis_cli = LoginManager(), Cache()
WORKING_DIR = os.path.abspath(os.getcwd())
TEMP_PATH = os.path.join(WORKING_DIR, 'static', 'avatars')


def create_app(config_name):
    app = Flask(__name__)
    app.logger.info("Starting app")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.login_view = 'auth.login'

    storing = 'http://localhost:5000/static/avatars'
    StoreManager.register(
        'fs',
        functools.partial(FileSystemStore, TEMP_PATH, storing),
        default=True
    )

    logging.basicConfig(
        filename="chariot_log.log",
        level=logging.DEBUG,
        encoding='utf-8'
    )

    app.logger.info(" Initializing App for mail, moment, db and login_manager")
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    app.logger.info("Initializing the blueprint of auth")
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from prod import prod as prod_blueprint
    app.register_blueprint(prod_blueprint, url_prefix='/p')

    with app.app_context():
        db.create_all()


    return app

config_name = (os.getenv('FLASK_CONFIG') or 'default').lower()
app = create_app(config_name)
app.logger.info("App Initializing done")
migrate = Migrate(app, db)



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
