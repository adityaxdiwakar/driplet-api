import sys

sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
sys.path.append('/'.join(sys.path[0].split('/')[0:-2]))

import a_api 
import db

#making the account
x = a_api.make_account({
    "email": "test@test.com",
    "username": "test",
    "password": "testing_password"
})

#confirming creation
if x.status_code != 201:
    db.reset()
    raise Exception(   
        f"Account creation did not return 201 response, instead returned {x.status_code}"
    )

user = x.json()
user_id = user["id"]
token = user["token"]

y = a_api.delete_account(user_id, "Definitely not the token")

if y.status_code != 401:
    db.reset()
    raise Exception(
        f"Account deletion did not return 401 response, instead returned {y.status_code}"
    )

db.reset()