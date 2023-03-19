#!/usr/bin/env python3
""" Script to contain decorators for the software """
from run import redis_cli
from functools import wraps
from .exception import UserNotLoggedIn


def confirm_login(func):
    @wraps(func)
    def wrapper(user_id, *args, **kwargs):
        email = (redis_cli.get(user_id)).decode('utf-8')
        if not email:
            return UserNotLoggedIn("User with the input not logged in")
        else:
            return func(*arg, **kwargs)
    return wrapper

