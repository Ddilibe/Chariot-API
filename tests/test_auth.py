#!/usr/bin/env python3
""" Script for testing the software for the auth blueprint """
from unitcase import TestCase
from auth.models import User
from run import db


class AuthTest(TestCase):
    def SetUp(self):
        pass
