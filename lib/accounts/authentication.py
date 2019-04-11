from passlib.apps import custom_app_context as pwd_context
from copy import copy

import jwt
import random
import string
import utils
import en_us


def make_password(given):
    return pwd_context.hash(given)


def check_password(given, stored):
    return pwd_context.verify(given, stored)


def salt(size=1024, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def user(user):
    fields = ['salt', 'password', 'services', '_id']
    for field in fields:
        try:
            user.pop(field)
        except KeyError:
            pass
    return user


def generate(user):
    mem_user = copy(user)
    mem_user.pop('salt')
    mem_user.pop('_id')
    mem_user.pop('password')
    token = jwt.encode(utils.encoder(mem_user),
                       user['salt'] + user['password'], algorithm='HS256')
    return token.decode('utf-8')


def verify(client_id, token):
    user = utils.encoder(utils.col.find({"id": client_id}))
    if len(user) == 0:
        return en_us.NOT_FOUND
    user = user[0]
    if user == None:
        return en_us.NOT_FOUND
    try:
        payload = jwt.decode(token, user['salt'] + user['password'], algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return en_us.AUTH_FAILED
    if 'id' in payload:
        if payload['id'] == user['id']:
            return 200
    return en_us.AUTH_FAILED
