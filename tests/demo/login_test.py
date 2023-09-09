#!/usr/bin/env python3
""" Script for testing an the login a section for the application """
import requests, json, time

# params = {
#     # "email_address": 'denever_rio@gmail.com',
#     # "password": "wearealwaysrunning"
#      "email_address": 'Eze_john@gmail.com',
#      "password": "wearferereealwaysrunning"
# }
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


params = {
    "email_address": get_user()['email_address'],
    "password": get_user()['password']
}
req = requests.post("http://localhost:5000/auth/login", json=params)
print(req.text)
value = req.json()
headers = {
    "Authorization": value.get('Authorization')
}
# wq = requests.post(f"http://localhost:5000/cart/{req.json()['Key']}/checkout")
# print(wq.text)
# req = requests.get("http://localhost:5000/auth/check")
# print(req.json())
req = requests.get("http://localhost:5000/auth/check", headers=headers)
print(req.text)

req = requests.post("http://localhost:5000/auth/newsletter", headers=headers)
print(req.text)

req = requests.delete("http://localhost:5000/auth/newsletter", headers=headers)
print(req.text)

req = requests.get("http://localhost:5000/auth/merchant", headers=headers)
print(req.text)

# params = {
#     'number': 329832929874234, 'exp_month':12, "exp_year":2028, 'cvc':232
# }
# req = requests.post("http://localhost:5000/auth/addcreditcard", headers=headers, json=params)
# print(req.text)

# req = requests.post("http://localhost:5000/auth/logout", headers=headers)
# print(req.text)
time.sleep(60)
