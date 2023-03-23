#!/usr/bin/env python3
""" Script for testing the software for the auth blueprint """
import os
import json
from uuid import uuid4
from flask import url_for
from random import randint
from auth.models import User
from unittest import TestCase
from run import db, app, redis_cli


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
        assert user.status_code == 200

    def test_login_with_unregistered_user(self):
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

    def test_login_and_logout_into_database(self):
        new_user = {i:self.user[i] for i in ['email_address', "password", "user_name"]}
        with self.client as c:
            req = c.post(self.app.url_for('auth.login'), json=new_user)
            assert req.json['Login'] == "Successful"
            assert req.json['Key'] == (redis_cli.get(new_user['user_name'])).decode('utf-8')
            assert req.status_code == 200
            assert req.json['Message'] == f"User {new_user['email_address']} has login in"
        with self.client as c:
            user_id = (redis_cli.get(new_user['user_name'])).decode('utf-8')
            server = f"{self.app.config['PREFERRED_URL_SCHEME']}"
            server += f"://{self.app.config['SERVER_NAME']}"
            logout = server + f"/auth/logout/{user_id}"
            assert logout == self.app.url_for('auth.logout', user_id=user_id)
            req = c.post(self.app.url_for('auth.logout', user_id=user_id))
            assert req.json['Logout'] == "Successful"
            assert req.status_code == 200

    def test_logout_with_unregistered_user(self):
        with self.client as c:
            req = c.post(self.app.url_for('auth.logout', user_id=str(uuid4())))
            assert req.json['Logout'] == "Logout is Unsuccessful"
            assert req.status_code == 403

    def test_signup_with_incomplete_data(self):
        with self.client as c:
            new_user = self.get_user(jam=44)
            del new_user['user_name']
            req = c.post(self.app.url_for('auth.signup'), json=new_user)
            assert req.json['Signup'] == "Failure"
            assert req.json["Message"] == "Invalid credential for signup"
            assert req.status_code == 400



    def tearDown(self):
        db.session.remove()
        db.drop_all()
