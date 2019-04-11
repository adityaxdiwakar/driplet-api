import a_api
import db

#making the account
x = a_api.make_account({
    "email": "test@test.com",
    "password": "testing_password"
})

#checking the server response
if x.status_code != 400:
    db.reset()
    raise Exception(
        f"Account creation w/ no username did not return 400 response, instead returned {x.status_code}"
    )

db.reset()