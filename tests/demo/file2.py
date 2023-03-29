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
all_products = requests.get("http://localhost:5000/p/prod/all")
for prod in all_products['products']:
    value = {
        "add_to_cart":{
            "name": id,
            "number": randint(0, 9)
        }
    }
    into_cart = requests.post(f"http://localhost:5000/cart/act/{new_user.json()['Key']}", json=value)
    print(into_cart.json())
display = requests.get(f"http://localhost:5000/cart/{new_user.json()['Key']}/all")
print(display.json())
buy_the = requests.post(f"http://localhost:5000/cart/{new_user.json()['Key']}/checkout")
