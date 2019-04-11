import a_api 

#making the account
x = a_api.make_account({
    "email": "test@test.com",
    "username": "test",
    "password": "testing_password"
})

#confirming creation
if x.status_code != 201:
    raise Exception(   
        f"Account creation to test login did not return 201 response, instead returned {x.status_code}"
    )

#testing login
user = x.json()

y = a_api.login_account({
    "username": "test",
    "password": "testing_password"
})

if y.status_code != 200:
    raise Exception(
        f"Login with valid account did return 200 response, instead returned {x.status_code}"
    )

l_user = y.json()

if user["token"] != l_user["token"]:
    raise Exception(
        f"Registered vs Login user token mismatch"
    )

if user["id"] != l_user["id"]:
    raise Exception(
        f"Registered vs Login user id mismatch"
    )

#cleaning up the account
user = x.json()
user_id = user["id"]
token = user["token"]

x = a_api.delete_account(user_id,token)

if x.status_code != 204:
    raise Exception(
        f"Account cleanup did not return 204 response, instead raised {x.status_code}"
    )

#confirming the account is cleaned up
x = a_api.get_account(user_id, token)

if x.status_code != 404:
    raise Exception(
        f"Account cleanup check did not return 404 response, instead raised {x.status_code}"
    )