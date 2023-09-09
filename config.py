#!/usr/bin/env python3
""" Script for the configuration class """
import os
from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    load_dotenv()
    TLS_VAR = ['true', 'on', '1']
    SECRET_KEY = os.getenv('SECERT_KEY', "Iwasoutwiththeboysdidntknowtillwecircleofgirlslaughingmiketurninhernameupsingingcarolina")
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in TLS_VAR
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = "[Chariot API]"
    FLASKY_MAIL_SENDER = "Chariot Admin <chariotadmin@chariot.com>"
    FLASKY_ADMIN = os.getenv('FLASKY_ADMIN')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_CURSORCLASS = os.getenv('MYSQL_CURSORCLASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "sqlalchemy"
    SESSION_PERMANENT = True
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
    JWT_HEADER_TYPE = "Chariot"
    JWT_ACCESS_TOKEN_EXPIRES = 3000
    THE_DATABASE = "sqlite" # It can be sqlite or mysql

    def init(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    ALONE = f"sqlite:///{os.path.join(BASE_DIR, 'data-dev.sqlite')}"
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or ALONE


class TestingConfig(Config):
    TESTING = True
    DB_NAME = "TEST_DATABASE_URL"
    SQLALCHEMY_DATABASE_URI = os.getenv(DB_NAME) or "sqlite://"

class ProductionConfig(Config):
    ALONE = "sqlite:///" + os.path.join(BASE_DIR, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or ALONE
    # DATABASE_URI = "sqlhost"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}

load_dotenv()
