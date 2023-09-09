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

headers = {
    'Authorization':"Chariot eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODRkZjUyY2EtZDdiYS00YzIyLWIxODYtZTZlMDEzMzdmOTVhIiwiZXhwIjoxNjk0Mjc4MTMyfQ.on5oqUd25U3-NNaCqCJ_IrwTyV2Tx9wQG_e-uozn-mM"
}
req = requests.get("http://127.0.0.1:5000/auth/logout", headers=headers)
print(req.json())
