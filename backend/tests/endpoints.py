ROOT = "http://127.0.0.1:3141/endpoints"

def services(clientid):
    return f"{ROOT}/{clientid}/services"

def service(clientid, serviceid):
    return f"{ROOT}/{clientid}/services/{serviceid}"

def login():
    return f"{ROOT}/login"

def verify(clientid):
    return f"{ROOT}/accounts/{clientid}/verify"

def register():
    return f"{ROOT}/register"