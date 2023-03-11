#!/usr/bin/env python3
""" Script for testing an the login a section for the application """
import requests, json


params = {
    "email_address": 'Eze_john@gmail.com',
    "user_name": 'johnny',
    "first_name": "John",
    "last_name": "Eze",
    "phone_number": 443903948930232,
    "gender": "female",
    "password": "wearferereealwaysrunning"
}

req = requests.post("http://127.0.0.1:5000/auth/signup", json=params)
print(req.json())
