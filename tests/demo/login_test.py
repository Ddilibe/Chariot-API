#!/usr/bin/env python3
""" Script for testing an the login a section for the application """
import requests, json


params = {
    # "email_address": 'denever_rio@gmail.com',
    # "password": "wearealwaysrunning"
     "email_address": 'Eze_john@gmail.com',
     "password": "wearferereealwaysrunning"
}

req = requests.post("http://127.0.0.1:5000/auth/login", json=params)
print(req.json())
req = requests.get("http://localhost:5000/auth/check")
print(req.json())
