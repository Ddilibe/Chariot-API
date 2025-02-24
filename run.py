#!/usr/bin/env python3
""" Script for running the whole operation on chariot """
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from utils.rediscli import Cache
from flask_moment import Moment
from dotenv import load_dotenv
from flask_mail import Mail
from flasgger import Swagger
from config import config
from flask import Flask
import stripe
import os


load_dotenv()
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

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
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

@app.cli.command(help="Run the tests for the app.")
def tests():
    import unittest
    tests = unittest.TestLoader().discover("tests/", pattern="tests_auth/test*.py", top_level_dir="tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    CONFIG = config[config_name]()
    # os.remove(os.getenv(env.upper()))
    
    

app.logger.info("App Initializing done")

