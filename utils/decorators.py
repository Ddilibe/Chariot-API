#!/usr/bin/env python3
""" Script to contain decorators for the software """
from run import redis_cli
from functools import wraps
from .exception import UserNotLoggedIn
from auth.models import User


def user_has_loggedin(user_id):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            email = redis_cli.get(user_id)
            if not email:
                raise UserNotLoggedIn("User Has Not LoginIn")
            email = email.decode("utf-8")
            user = User.query.filter_by(email_address=email).first_or_404()
            kwargs['user'] = user
            return func(*args, **kwargs)
        return wrapper
    return decorator

