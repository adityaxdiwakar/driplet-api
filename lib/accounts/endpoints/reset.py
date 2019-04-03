from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import en_us

class reset(Resource):
    def post(self, clientid):
        r = account_utils.password_reset(clientid)        
        if r == 404:
            return en_us.NOT_FOUND
        if r == 400:
            return en_us.BAD_REQUEST
        return en_us.RESET_REQ_MADE

{'personalizations': [{'to': [{'email': 'new@new.com'}], 'subject': 'Reset Password Request'}], 'from': {'email': 'support@driplet.cf'}, 'content': [{'type': 'text/html', 'value': "<h1>Password reset</h1><br><p>Reset your Driplet account password by clicking <a href='https://driplet.cf/reset?=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmF0aW9uIjoxNTU0MzMyNzk5fQ.dnv0XEY7pK4BU-lYM7XStzLQlZpdkAU3bHzjzJ9_cp8'>here!</a>"}]}