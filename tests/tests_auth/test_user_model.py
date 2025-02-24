#!/bin/env python3
from auth.models import GenderEnum, User, CreditCard
from dotenv import load_dotenv
from unittest import TestCase
from tests.layer import DataLayer
from uuid import uuid4
from run import app
from run import db
import os

load_dotenv()

class UnitDUserTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.datalayer = DataLayer(db, app)
        cls.user_details = cls.datalayer.user_1
        if not cls.datalayer.get_user(cls.user_details.get('user_id')):
            cls.datalayer.create_user(cls.user_details)
        cls.user_id = cls.datalayer.get_user(cls.user_details.get("user_id"))

    @classmethod
    def tearDownClass(cls):
        cls.datalayer.rollover()

    def test_a_a_user_variable_match(self):
        self.a
        self.assertEqual(self.user_id.first_name, self.user_details['first_name'])
        self.assertEqual(self.user_id.user_name, self.user_details['user_name'])
        self.assertEqual(self.user_id.last_name, self.user_details['last_name'])
        self.assertEqual(self.user_id.profile_picture, self.user_details['profile_picture'])
        self.assertEqual(self.user_id.country, self.user_details['country'])
        self.assertEqual(self.user_id.gender, self.user_details['gender'])
        self.assertEqual(self.user_id.email_address, self.user_details['email_address'])
        
    def test_a_b_user_variables_match_after_an_update(self):
        update_user = self.datalayer.update_user
        for key, value in update_user.items():
            self.datalayer.edit_user(self.user_id.user_id, key, value)
        self.assertEqual(self.user_id.first_name, update_user['first_name'])
        self.assertEqual(self.user_id.user_name, update_user['user_name'])
        self.assertEqual(self.user_id.last_name, update_user['last_name'])
        self.assertEqual(self.user_id.profile_picture, update_user['profile_picture'])
        self.assertEqual(self.user_id.country, update_user['country'])
        self.assertEqual(self.user_id.gender, update_user['gender'])
        self.assertEqual(self.user_id.email_address, update_user['email_address'])
        

class UnitCreditCartTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.datalayer = DataLayer(db, app)
        cls.user_details, cls.creditcard_details = cls.datalayer.user_1, cls.datalayer.credit_card
        if not cls.datalayer.get_user(cls.user_details.get('user_id')):
            cls.datalayer.create_user(cls.user_details)
        cls.user_id = cls.datalayer.get_user(cls.user_details.get("user_id"))
        if not cls.datalayer.get_credit_card(cls.creditcard_details.get('credit_card_id')):
            cls.datalayer.create_credit_card(cls.creditcard_details, cls.user_id)
        cls.user_credit_card = cls.user_id.credit_card
 
    def test_b_credit_card_variables(self):
        self.assertEqual(self.user_credit_card.exp_month, self.creditcard_details['exp_month'])
        self.assertEqual(self.user_credit_card.exp_year, self.creditcard_details['exp_year'])
        self.assertEqual(self.user_credit_card.number, self.creditcard_details['number'])
        self.assertEqual(self.user_credit_card.cvc, self.creditcard_details['cvc'])

    @classmethod
    def tearDownClass(cls):
        cls.datalayer.rollover()


class ZZZZZTestCase(TestCase):
    
    def test_zzz_clean_database(self):
        datalayer = DataLayer(db, app)
        datalayer.clean()