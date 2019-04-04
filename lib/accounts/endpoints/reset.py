from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import en_us
import time
import utils

class reset(Resource):
    def post(self):
        args = utils.gen_fields(reqparse.RequestParser(), ['identification'])
        r = account_utils.password_reset(args["identification"])        
        if r == 404:
            return en_us.NOT_FOUND
        if r == 400:
            return en_us.BAD_REQUEST
        return en_us.RESET_REQ_MADE