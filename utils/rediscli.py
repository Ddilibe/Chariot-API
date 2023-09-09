#!/usr/bin/env python3
""" Script for Writing basic redis commands with python """
import os
import redis
from uuid import uuid4

class Cache(object):
    """docstring for Cache"""
    def __init__(self):
        """ Method for initiating the class instance """
        env = os.environ.get('REDIS_URL')
        self._redis = redis.from_url(env) if env else redis.Redis(decode_responses=True)
        # self.flushdb = self._redis.flushdb()

    def init_app(app):
        """ Method for initializing the flask_app """
        pass

    def store(self, data) -> str:
        """ A method for storing a key value pair in the redis server """
        from run import db
        from auth.models import User

        key = str(uuid4())
        self._redis.set(key, data, ex=10000000)
        return key

    def get(self, key: str, fn=None):
        """ A method for reteriving the value associated with the key """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def session(self, key, data):
        self._redis.set(key, data, ex=120)

    def dele(self, key):
        self._redis.delete(key)

    def check(self, value):
        if self._redis.exists(value):
            return True
        return False
