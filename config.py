#!/usr/bin/env python3
""" Script for the configuration class """
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    TLS_VAR = ['true', 'on', '1']
    SECRET_KEY = os.environ.get('SECERT_KEY') or "Word that is complex"
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in TLS_VAR
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = "[Chariot API]"
    FLASKY_MAIL_SENDER = "Chariot Admin <chariotadmin@chariot.com>"
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')
    MYSQL_CURSORCLASS = os.environ.get('MYSQL_CURSORCLASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "sqlalchemy"
    SESSION_PERMANENT = True
    THE_DATABASE = "sqlite" # It can be sqlite or mysql
    DATABASENAME = ""

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = False
    ALONE = f"sqlite:///{os.path.join(basedir, 'data-dev.sqlite')}"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or ALONE


class TestingConfig(Config):
    TEST = True
    DB_NAME = "TEST_DATABASE_URL"
    DATABASENAME = "testing.sqlite"
    ALONE = f"sqlite:///{os.path.join(basedir, DATABASENAME)}"
    SQLALCHEMY_DATABASE_URI = os.environ.get(DB_NAME) or ALONE

class ProductionConfig(Config):
    ALONE = "sqlite:///" + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or ALONE
    # DATABASE_URI = "sqlhost"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
