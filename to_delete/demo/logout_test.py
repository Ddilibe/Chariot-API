#!/usr/bin/env python3
""" Script for testing an the login a section for the application """
import requests, json


params = {
    "email_address": 'denever_rio@gmail.com',
    "user_name": 'Denever_rio',
    "first_name": "Denever",
    "last_name": "Rosario",
    "phone_number": 48393948930232,
    "gender": "male",
    "password": "wearealwaysrunning"
}

req = requests.post("http://127.0.0.1:5000/auth/logout/ccbb8067-23a5-rereer43b5-86df-5210ca99ca3a")
print(req.text)
