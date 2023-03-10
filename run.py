#!/usr/bin/env python3
""" Script for running the whole operation on chariot """
from config import config
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
import os


mail, moment, db = Mail(), Moment(), SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    return app

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name.lower())
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict()
