import requests
import endpoints
import utils
import json
import time


start = utils.dialog("Checking account creation...", end=" ")
#make the original account
r = requests.post(
    endpoints.register(),
    data = {
        "email": "aditya@diwakar.io",
        "username": "driplet",
        "password": "very_strong_dev_password"
    }
)
if r.status_code != 200:
    utils.dialog("Received a non-200 status code")
    assert ValueError
else:
    utils.dialog(f"{int(time.time() - start)}s")

utils.push_user(r.json())

start = utils.dialog("Checking account creation w/ no email...", end=" ")
#make an account with no email
r = requests.post(
    endpoints.register(),
    data = {
        "email": None,
        "username": "driplet_pass",
        "password": "super_duper_strong_dev_password"
    }
)
if r.status_code != 400:
    utils.dialog("Received a non-400 status code")
    assert ValueError
else:
    utils.dialog(f"{int(time.time() - start)}")


