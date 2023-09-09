#!/usr/bin/env python3
""" Script for testing an the login a section for the application """
import requests, json, base64
from random import randint


# with open("some.png", 'rb') as img_file:
    # img_str = base64.b64encode(img_file.read())

def get_user(jam=None):
        with open(f"populate/users.json", "r") as file:
            file = json.loads(file.read())
            i = file[randint(3, jam if jam > 3 else jam + 4) if jam else 2]
            i = {
                "profile_picture": "http://placehold.it/32x32",
                "first_name": "Wilda ",
                "last_name": "Yates",
                "user_name": "sunt",
                "gender": "female",
                "email_address": "wildayates@olympix.com",
                "phone_number": "(973) 534-2869",
                "newletter_subscription": True,
                "password": "consectetur esse",
                "account_status": False
            }
            del i["profile_picture"]
            i["newletter_subscription"] = (
                "true" if i["newletter_subscription"] else "false"
            )
            i["account_status"] = "veri" if i["account_status"] else "not_ver"
            return i

# params = {
#     "email_address": 'abudhi_micheal@gmail.com',
#     "user_name": 'James',
#     "first_name": "Abuchi",
#     "last_name": "Micheal",
#     "phone_number": 429482942889,
#     "gender": "male",
#     "password": "babbyicantfigureyouout",
#     "profile_picture": img_str.decode('utf-8'),
#     "picture_name": "some.png"
# }

params = get_user(jam=34)
params['country'] = "US"
params['is_merchant'] = False
"""
{
    "profile_picture": "http://placehold.it/32x32",
    "first_name": "Randi ",
    "last_name": "Mayer",
    "user_name": "sit",
    "gender": "female",
    "email_address": "randimayer@olympix.com",
    "phone_number": "(950) 439-3925",
    "newletter_subscription": true,
    "password": "nulla qui",
    "account_status": false
  }
"""

req = requests.post("http://localhost:5000/auth/signup", json=params)
print(req.json())
# wq = requests.post(f"http://localhost:5000/cart/{req.json()['Key']}/checkout")
# print(wq.json())
