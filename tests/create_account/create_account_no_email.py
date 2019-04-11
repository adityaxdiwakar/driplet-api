import a_api

#making the account
x = a_api.make_account({
    "username": "test",
    "password": "testing_password"
})

#checking the server response
if x.status_code != 400:
    raise Exception(
        f"Account creation w/ no email did not return 400 response, instead returned {x.status_code}"
    )
