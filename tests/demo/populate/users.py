#!/usr/bin/env python3
""" Script for populating the database filled with users """
import requests
import json
import time
import asyncio
import uuid

def added_to_database(value):
    req = requests.post(f'http://localhost:5000/auth/{uuid.uuid4()}/newsletter')
    print(req.json())

with open('users.json', 'r') as file:
    file = json.loads(file.read())
    for i in file:
        del i['profile_picture']
        i["newletter_subscription"] = "true" if i["newletter_subscription"] else "false"
        i["account_status"] = "veri" if i["account_status"] else "not_ver"
        added_to_database(i)
        # req = requests.post('http://localhost:5000/auth/signup', json=i)
        # print(req.json())
        # time.sleep(10)
# [{'first_name': 'Delacruz ', 'last_name': 'Swanson', 'user_name': 'elit', 'gender': 'male', 'email_address': 'delacruzswanson@olympix.com', 'phone_number': '(922) 506-2730', 'newletter_subscription': 'false', 'password': 'laborum quis', 'account_status': 'not_ver'}, {'first_name': 'Adeline ', 'last_name': 'Macias', 'user_name': 'aliqua', 'gender': 'female', 'email_address': 'adelinemacias@olympix.com', 'phone_number': '(931) 532-3844', 'newletter_subscription': 'true', 'password': 'laborum commodo', 'account_status': 'not_ver'}, {'first_name': 'Brandi ', 'last_name': 'Bray', 'user_name': 'veniam', 'gender': 'female', 'email_address': 'brandibray@olympix.com', 'phone_number': '(828) 544-3411', 'newletter_subscription': 'true', 'password': 'eu dolor', 'account_status': 'not_ver'}, {'first_name': 'Reese ', 'last_name': 'Duke', 'user_name': 'cupidatat', 'gender': 'male', 'email_address': 'reeseduke@olympix.com', 'phone_number': '(887) 597-2677', 'newletter_subscription': 'true', 'password': 'tempor qui', 'account_status': 'veri'}, {'first_name': 'Harvey ', 'last_name': 'Perry', 'user_name': 'amet', 'gender': 'male', 'email_address': 'harveyperry@olympix.com', 'phone_number': '(940) 557-3350', 'newletter_subscription': 'true', 'password': 'anim amet', 'account_status': 'not_ver'}, {'first_name': 'Golden ', 'last_name': 'Melton', 'user_name': 'aute', 'gender': 'male', 'email_address': 'goldenmelton@olympix.com', 'phone_number': '(970) 437-3285', 'newletter_subscription': 'false', 'password': 'ipsum elit', 'account_status': 'not_ver'}, {'first_name': 'Gillespie ', 'last_name': 'Conway', 'user_name': 'do', 'gender': 'male', 'email_address': 'gillespieconway@olympix.com', 'phone_number': '(991) 406-3159', 'newletter_subscription': 'false', 'password': 'anim aute', 'account_status': 'veri'}, {'first_name': 'Stephenson ', 'last_name': 'Koch', 'user_name': 'ullamco', 'gender': 'male', 'email_address': 'stephensonkoch@olympix.com', 'phone_number': '(834) 548-3592', 'newletter_subscription': 'false', 'password': 'reprehenderit Lorem', 'account_status': 'not_ver'}]

