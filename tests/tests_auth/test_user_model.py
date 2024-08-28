#!/bin/env python3
from auth.models import GenderEnum, User, CreditCart
from dotenv import load_dotenv
from unittest import TestCase
from uuid import uuid4
from run import db
import os

load_dotenv()

class UnitUserTestCase(TestCase):


    def setUp(self) -> None:
        self.user_details = {
            'first_name': "Emeka", 'user_name': 'Emike', "last_name": "Eze", "id": str(uuid4()),
            'profile_picture': f"{os.getenv('MEDIASTORAGE')}/Emike/trerieeorieferf.jpeg",
            "password" : "Passwording", "country": "Nigeria", "phone_number": 2343455346,
            "gender": GenderEnum.male, "email_address": "emeka.ere@gmail.com"
        }
        new_user = User(**self.user_details)
        db.session.add(new_user)
        db.session.commit()
        self.userid = User.query.filter_by(email_address=self.user_details['email_address']).first_or_404()

    def test_user_first_name(self):
        self.assertEqual(self.userid.first_name, self.user_details['first_name'])

    def test_user_user_name(self):
        self.assertEqual(self.userid.user_name, self.user_details['user_name'])

    def test_user_last_name(self):
        self.assertEqual(self.userid.last_name, self.user_details['last_name'])

    def test_user_profile_picture(self):
        self.assertEqual(self.userid.profile_picture, self.user_details['profile_picture'])
    
    def test_user_country(self):
        self.assertEqual(self.userid.country, self.user_details['country'])

    def test_user_gender(self):
        self.assertEqual(self.userid.gender, self.user_details['gender'])

    def test_email_address(self):
        self.assertEqual(self.userid.email_address, self.user_details['email_address'])

    def tearDown(self):
        db.session.delete(self.userid)
        db.commit()
    
class UnitCreditCartTestCase(TestCase):


    def setUp(self) -> None:
        self.user_details = {
            'first_name': "Emeka", 'user_name': 'Emike', "last_name": "Eze", "id": str(uuid4()),
            'profile_picture': f"{os.getenv('MEDIASTORAGE')}/Emike/trerieeorieferf.jpeg",
            "password" : "Passwording", "country": "Nigeria", "phone_number": 2343455346,
            "gender": GenderEnum.male, "email_address": "emeka.ere@gmail.com"
        }
        self.credit_card = {
            "number": 439898230783298, "exp_month": 9, "exp_year": 2024, "cvc": 438
        }
        new_user = User(**self.user_details)
        db.session.add(new_user)
        new_credit = CreditCart(**self.credit_card)
        new_credit.user_id = new_user.id
        db.session.add(new_credit)
        db.session.commit()
        self.user = User.query.filter_by(email_address=self.user_details['email_address']).first_or_404()
        self.credit = CreditCart.query.filter_by(id=self.user.id).first_or_404()

    def test_exp_month(self):
        self.assertEqual(self.credit.exp_month, self.credit_card['exp_month'])

    def test_exp_year(self):
        self.assertEqual(self.credit.exp_year, self.credit_card['exp_year'])

    def test_number(self):
        self.assertEqual(self.credit.number, self.credit_card['number'])

    def test_cvc(self):
        self.assertEqual(self.credit.cvc, self.credit_card['cvc'])

    def tearDown(self) -> None:
        db.session.delete(self.credit)
        db.session.delete(self.user)
        db.commit()
        return super().tearDownClass()