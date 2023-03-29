#!/usr/bin/env python3
""" Script for testing user 1 """
import json
import time
import requests
from random import randint

def get_user(jam=None):
        with open(f"populate/users.json", "r") as file:
            file = json.loads(file.read())
            # i = file[randint(3, jam if jam > 3 else jam + 4) if jam else 2]
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
            i['country'], i['is_merchant'] = "US", False
            return i

def get_product(a, b):
    with open(f"populate/products.json", "r") as file:
        file = json.loads(file.read())
        i = file[a:b]
        return i

user_param = get_user()
create_user = requests.post("http://localhost:5000/auth/signup", json=user_param)
print(create_user.json())
new_user = requests.post("http://localhost:5000/auth/login", json=user_param)
print(new_user.json())
print("\n\nLogining user\n\nUser is not a merchant\n\nWe will make the user merchant\n\n")
requests.post(f"http://localhost:5000/auth/{new_user.json()['Key']}/merchant")
print("Creating a product")
product_1 = get_product(0,4)
for i in product_1:
    new_product = requests.post(f"http://localhost:5000/p/prod/{new_user.json()['Key']}/c", json=i)
    print(new_product.json())

