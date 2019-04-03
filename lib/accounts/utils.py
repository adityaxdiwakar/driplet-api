import random
import json
import os
import pymongo
import utils
import requests as r

def template(email, link):
    return {
        "personalizations": [
            {
                "to": [
                    {
                        "email": email
                    }
                ],
                "subject": "Reset Password Request"
            }
        ],
        "from": {
            "email": "support@driplet.cf"
        },
        "content": [
            {
                "type": "text/html",
                "value": "<h1>Password reset</h1><br><p>" + link + "</p>"
            }
        ]
    }

import string
import random
import jwt
import time

def password_reset(userid):
    x = utils.col.find({"id": userid})
    if x.count == 0:
        return 404 #not found
    user = utils.encoder(x)[0]
    email = user["email"]
    encoded_jwt = jwt.encode({'expiration': int(time.time()) + 3600}, user["salt"], algorithm='HS256')
    encoded_jwt = encoded_jwt.decode('utf-8')
    e_tem = template(email, f"https://driplet.cf/reset?={encoded_jwt}")
    s = r.post(
        "https://api.sendgrid.com/v3/mail/send",
        json = e_tem,
        headers = {
            "Authorization": "Bearer " + os.getenv("API_KEY"),
            "Content-Type": "application/json"
        }
    )
    if s.status_code != 202:
        return 400

def get_user_id():
    while True:
        r = random.randint(1000000000, 9999999999)
        if utils.col.find({"id": 'u' + str(r)}).count() == 0:
            return 'u' + str(r)
