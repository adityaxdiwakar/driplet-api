import requests

def make_account(payload):
    return requests.post("http://localhost:3141/endpoints/register",
                      data=payload)

def login_account(payload):
    return requests.post("http://localhost:3141/endpoints/login",
                      data=payload)

def verify_account(user_id, token):
    return requests.get(f"http://localhost:3141/endpoints/accounts/{user_id}/verify",
                     headers = {"authorization": token})

def get_account(user_id, token):
    return requests.get(f"http://localhost:3141/endpoints/accounts/{user_id}",
                     headers= {"authorization": token})

def update_account(payload, user_id, token):
    return requests.patch(f"http://localhost:3141/endpoints/accounts/{user_id}",
                      payload = payload,
                      headers = {"authorization": token})

def delete_account(user_id, token):
    return requests.delete(f"http://localhost:3141/endpoints/accounts/{user_id}",
                        headers = {"authorization": token})
