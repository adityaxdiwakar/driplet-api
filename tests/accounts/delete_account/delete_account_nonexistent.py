import sys

sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
sys.path.append('/'.join(sys.path[0].split('/')[0:-2]))

import a_api 
import db

y = a_api.delete_account("", "")

if y.status_code != 404:
    db.reset()
    raise Exception(
        f"Account deletion did not return 404 response, instead returned {y.status_code}"
    )

db.reset()