ROOT = "localhost:3141/endpoints"

def LOGIN():
    return f"{ROOT}/login"

def REGISTER():
    return f"{ROOT}/register"

def SERVICES(client_id):
    return f"{ROOT}/{client_id}/services"

def SERVICE(client_id, service_id):
    return f"{ROOT}/{client_id}/services/{service_id}"

def ACCOUNT(client_id):
    return f"{ROOT}/accounts/{client_id}"

def VERIFY(client_id):
    return f"{ROOT}/accounts/{client_id}/verify"