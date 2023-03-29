#!/usr/bin/env python3
""" Script for testing the auth user models """
import json
import unittest
from run import db, app
from auth.models import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.user = self.get_user()
        self.create_user()

    def get_user(self, jam=None):
        with open(f'tests/demo/populate/users.json', 'r') as file:
            file = json.loads(file.read())
            i = file[randint(3, jam if jam > 3 else jam+4) if jam else 2]
            del i['profile_picture']
            i["newletter_subscription"] = "true" if i["newletter_subscription"] else "false"
            i["account_status"] = "veri" if i["account_status"] else "not_ver"
            i['country'], i['is_merchant'] = "US", False
            return i

    def create_user(self):
        user_attributes = self.user
        new_user = User(**self.user)
        db.session.add(new_user)
        db.session.commit()

    def test_a_user_name(self):
        user = User.query.all()[0]
        assert user.user_name == self.user['user_name']

    def test_a_first_name(self):
        user = User.query.all()[0]
        assert user.first_name == self.user['first_name']

    def test_a_last_name(self):
        user = User.query.all()[0]
        assert user.last_name == self.user['last_name']

    def test_a_email_address(self):
        user = User.query.all()[0]
        assert user.email_address == self.user['email_address']

    # @unittest.expectedFailure
    def test_a_password(self):
        user = User.query.all()[0]
        with self.assertRaises(AttributeError):
            user.password()

    def test_a_phone_number(self):
        user = User.query.all()[0]
        assert user.phone_number == self.user['phone_number']

    def test_a_gender(self):
        user = User.query.all()[0]
        assert user.gender.name == self.user['gender']

    # def test_password()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
