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
        f"Account creation did not return 201 response, instead returned {x.status_code}"
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