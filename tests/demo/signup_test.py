#!/usr/bin/env python3
""" Script for testing an the login a section for the application """
import requests, json, base64


with open("some.png", 'rb') as img_file:
    img_str = base64.b64encode(img_file.read())



params = {
    "email_address": 'abudhi_micheal@gmail.com',
    "user_name": 'James',
    "first_name": "Abuchi",
    "last_name": "Micheal",
    "phone_number": 429482942889,
    "gender": "male",
    "password": "babbyicantfigureyouout",
    "profile_picture": img_str.decode('utf-8'),
    "picture_name": "some.png"
}

req = requests.post("http://127.0.0.1:5000/auth/signup", json=params)
print(req.json())
