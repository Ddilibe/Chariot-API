#!/usr/bin/env python3
""" Script for testing the software for the auth blueprint """
import json
import os
from run import db, app
from flask import url_for
from random import randint
from auth.models import User
from unittest import TestCase


os.environ['FLASK_CONFIG'] = "testing"


class AuthTest(TestCase):

    def setUp(self):
        self.config_name = (os.getenv('FLASK_CONFIG') or 'default').lower()
        self.app, self.user = app, self.get_user()
        self.client = self.app.test_client()
        db.create_all()
        self.populate_database()

    def get_user(self, jam=None):
        with open(f'tests/demo/populate/users.json', 'r') as file:
            file = json.loads(file.read())
            i = file[randint(3, jam if jam > 3 else jam+4) if jam else 2]
            del i['profile_picture']
            i["newletter_subscription"] = "true" if i["newletter_subscription"] else "false"
            i["account_status"] = "veri" if i["account_status"] else "not_ver"
            return i


    def test_for_url(self):
        server = f"{self.app.config['PREFERRED_URL_SCHEME']}"
        server += f"://{self.app.config['SERVER_NAME']}"
        signup = server + f"/auth/signup"
        login = server + f"/auth/login"
        logout = server + f"/auth/logout"
        assert signup == self.app.url_for('auth.signup')
        assert login == self.app.url_for('auth.login')
        # assert logout == self.app.url_for('auth.logout')


    def test_create_user(self):
        new_user = self.get_user(jam=66)
        res = self.client.post(
            self.app.url_for('auth.signup'),
            data=json.dumps(new_user),
            mimetype="application/json"
        )
        user_attributes = {
            "Message": f"User {new_user['email_address']} has signed up",
            "last_name": new_user["last_name"],
            "first_name": new_user["first_name"],
            "user_name": new_user["user_name"],
            "gender": new_user["gender"],
            "email_address": new_user["email_address"],
            "phone_number": new_user['phone_number'],
            "Signup": "Successful"
        }
        new_user = {i:self.user[i] for i in ['email_address', "password"]}
        assert res.json == user_attributes

    def test_login_user(self):
        new_user = {i:self.user[i] for i in ['email_address', "password"]}
        user = self.client.post(
            self.app.url_for('auth.login'),
            data=json.dumps(new_user),
            mimetype="application/json"
        )
        assert user.json.get('Login') == "Successful"
        assert user.json.get('Message') == f"User {self.user['email_address']} has login in"
        self.app.logger.info(user.status_code)
        assert user.status_code == 201

    def test_login_with_for(self):
        new_user = self.get_user(jam=90)
        req = self.client.post(self.app.url_for('auth.login'),
            data=json.dumps(new_user),
            mimetype="application/json"
        )
        assert req.json.get('Login') != "Successful"
        assert req.json.get('Message') == f"User {new_user['email_address']} cannot login in"
        assert req.status_code == 401
        # new_user = User(**user_attributes)
        # db.session.add(new_user)
        # db.session.commit()

    def populate_database(self):
        user_attributes = self.user
        new_user = User(**self.user)
        db.session.add(new_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
