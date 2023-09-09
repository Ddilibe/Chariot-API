#!/usr/bin/env python
""" Script for the signals for the auth blueprint """
from .backend import verify_token, retrieve_user
from blinker import Namespace
import threading
import datetime


signal_namespace = Namespace()


token_about_to_expire = signal_namespace.signal('token-about-to-expire')

def handle_token_about_to_expire(sender, token, expiration_time):
    from run import db
    def action_to_occurs_before_token_expires():
        # Calculate the time remaining until token expiration
        current_time = datetime.datetime.utcnow()
        time_remaining = expiration_time - current_time
        # Schedule an action (e.g., log a message) shortly before token expiration
        if time_remaining.total_seconds() <= 0:
            user = retrieve_user()
            user.logged = False
            user.save()
            print(f"Token {token} has already expired.")
        else:
            print(f"Token {token} will expire in {time_remaining.total_seconds()} seconds.")

    # Create a thread to execute the action
    current_time = datetime.datetime.utcnow()
    time_remaining = expiration_time - current_time
    th = threading.Thread(target=action_to_occurs_before_token_expires)
    th.start()
    th.join(timeout=time_remaining.total_seconds())

# Connect the signal handler
token_about_to_expire.connect(handle_token_about_to_expire)
