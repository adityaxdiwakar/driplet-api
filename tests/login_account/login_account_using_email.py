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
        f"Account creation to test login did not return 201 response, instead returned {x.status_code}"
    )

#testing login
user = x.json()

y = a_api.login_account({
    "username": "test@test.com",
    "password": "testing_password"
})

if y.status_code != 200:
    db.reset()
    raise Exception(
        f"Login using email on valid account did return 200 response, instead returned returned {x.status_code}"
    )

l_user = y.json()

if user["token"] != l_user["token"]:
    db.reset()
    raise Exception(
        f"Registered vs Login user token mismatch (using email)"
    )

if user["id"] != l_user["id"]:
    db.reset()
    raise Exception(
        f"Registered vs Login user id mismatch (using email)"
    )

db.reset()