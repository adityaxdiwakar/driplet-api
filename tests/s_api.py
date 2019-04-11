import requests

def make_service(payload, user_id, token):
    return requests.post(f"http://localhost:3141/endpoints/{user_id}/services",
                      payload = payload,
                      headers = {"authorization": token})

def get_services(user_id, token):
    return requests.get(f"http://localhost:3141/endpoints/{user_id}/services",
                        headers = {"authorization": token})
            
def get_service(user_id, token, service_id):
    return requests.get(f"http://localhost:3141/endpoints/{user_id}/services/{service_id}",
                        headers = {"authorization": token})

