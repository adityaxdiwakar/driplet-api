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

y = a_api.login_account({})

if y.status_code != 400:
    db.reset()
    raise Exception(
        f"Login with no payload on valid account did return 400 response, instead returned returned {y.status_code}"
    )

db.reset()