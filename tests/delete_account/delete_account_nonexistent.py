import a_api 
import db

y = a_api.delete_account("", "")

if y.status_code != 400:
    db.reset()
    raise Exception(
        f"Account deletion did not return 404 response, instead returned {y.status_code}"
    )

db.reset()