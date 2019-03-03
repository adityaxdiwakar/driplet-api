from passlib.apps import custom_app_context as pwd_context
from lib.accounts import utils as account_utils

import jwt
import random
import string
import en_us
import copy

def make_password(given):
    return pwd_context.hash(given)

def check_password(given, stored):
    return pwd_context.verify(given, stored)

def salt(size=1024, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def user(user):
    user.pop('salt')
    user.pop('password')
    return user

def generate(user, salt):
    mem_user = copy.copy(user)
    mem_user.pop('salt')
    token = jwt.encode(mem_user, user['salt'], algorithm='HS256')
    return token.decode('utf-8')

def verify(client_id, token):
    user = account_utils.get(client_id)
    if user == None:
        return en_us.NOT_FOUND
    try:
        payload = jwt.decode(token, user['salt'], algorithms=['HS256'])
    except:
        return en_us.AUTH_FAILED
    if 'id' in payload:
        if payload['id'] == user['id']:
            return 200
    return en_us.AUTH_FAILED 