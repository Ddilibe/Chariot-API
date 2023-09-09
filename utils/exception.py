#!/usr/bin/env python3
""" Script for delcaring the exceptions for the application"""


class ProductWithoutCreator(Exception):
    pass

class ExcessProductInput(Exception):
    pass

class UnavaliableImageName(Exception):
    pass

class RequiredDataError(Exception):
    pass

class InvalidKeyError(Exception):
    pass

class UserNonExistError(Exception):
    pass

class ProductNotExistError(Exception):
    pass

class TagNotExistError(Exception):
    pass

class UnavaliableImageName(Exception):
    pass

class NotProductInstance(Exception):
    pass

class UserNotLoggedIn(Exception):
    pass

class NotAbleToBeAnAdminError(Exception):
    pass

class PasswordNotCorrectError(Exception):
    pass

class InvalidUserAttributes(Exception):
    pass
