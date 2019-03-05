import time
import json

def get_user():
    return json.load(
        open("backend/tests/test_creds.json", "r")
    )

def push_user(user):
    return json.dump(
        user,
        open("backend/tests/test_creds.json", "w"),
        indent = 4
    )

def dialog(prompt, end="\n"):
    print(prompt, end=end)
    return time.time()