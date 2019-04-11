import a_api

#making the account
x = a_api.make_account({})

#checking the server response
if x.status_code != 400:
    raise Exception(
        f"Account creation w/ no username did not return 400 response, instead returned {x.status_code}"
    )
