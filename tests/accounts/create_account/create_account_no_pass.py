import sys

sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
sys.path.append('/'.join(sys.path[0].split('/')[0:-2]))

import a_api
import db

#making the account
x = a_api.make_account({
    "email": "test@test.com",
    "username": "test"
})

#checking the server response
if x.status_code != 400:
    db.reset()
    raise Exception(
        f"Account creation w/ no password did not return 400 response, instead returned {x.status_code}"
    )

db.reset()