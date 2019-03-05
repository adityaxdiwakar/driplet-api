import requests
import endpoints
import utils
import json
import time

print("Sleeping for docker container bootup")
time.sleep(5)


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
if r.status_code != 201:
    utils.dialog(f"Received a non-200 status code ({r.status_code})")
    print(r.text)
    raise Exception("Could not create an account")
else:
    utils.dialog(f"{round(time.time() - start, 3)}s")

utils.push_user(r.json())

start = utils.dialog("Checking account creation w/ no email...", end=" ")
#make an account with no email
r = requests.post(
    endpoints.register(),
    data = {
        "username": "driplet_pass",
        "password": "super_duper_strong_dev_password"
    }
)
if r.status_code != 400:
    utils.dialog(f"Received a non-400 status code ({r.status_code})")
    assert ValueError
else:
    utils.dialog(f"{round(time.time() - start, 3)}")

start = utils.dialog("Checking account creation w/ no username...", end=" ")
#make an account with no password
r = requests.post(
    endpoints.register(),
    data = {
        "email": "email@example.com",
        "password": "super_duper_strong_dev_password"
    }
)
if r.status_code != 400:
    utils.dialog(f"Received a non-400 status code ({r.status_code})")
    assert ValueError
else:
    utils.dialog(f"{round(time.time() - start, 3)}")

start = utils.dialog("Checking account creation w/ no password...", end=" ")
#make an account with no password
r = requests.post(
    endpoints.register(),
    data = {
        "email": "email2@example.com",
        "username": "username"
    }
)
if r.status_code != 400:
    utils.dialog(f"Received a non-400 status code ({r.status_code})")
    assert ValueError
else:
    utils.dialog(f"{round(time.time() - start, 3)}")
