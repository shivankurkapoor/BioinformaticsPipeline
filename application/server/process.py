'''
Created by Shivankur Kapoot
Date : 12/22/2016
This module contains function to call pipeline process, and calling file download and upload
'''
import httplib2
from common.globalconst import *
from common.globalfunct import *
from database import *
from datetime import datetime, timedelta
from dateutil import parser
from database.domain.user import User
from oauth2client.client import Credentials
from database.domain.request import Request
from server.connect import renew_access_token
from googleapiclient.discovery import build
from apiclient import discovery


def download(request_id = ''):
    try:
        assert request_id
    except AssertionError:
        print 'User Id is missing'
        return INT_ERROR_GENERAL
    try:
        request = engine.query(Request).filter(user_id=request_id)
        if user:
            user_dict = user.__dict__
            credentials = Credentials.new_from_json(user_dict['credentials'])
            token_expiry = credentials['token_expiry']
            dexp = parser.parse(str(token_expiry))
            dexp = dexp.replace(tzinfo=None)
            dnow = datetime.now()

            if dexp < dnow:
                status_code, data = renew_access_token(client_id=credentials['client_id'],
                                                       client_secret=credentials['client_secret'],
                                                       refresh_token=credentials['refresh_token'],
                                                       )
                if status_code == INT_OK:
                    credentials['access_token'] = data['access_token']
                    credentials['token_expiry'] = datetime_util(
                        datetime.now() + timedelta(seconds=float(str(data['expires_in']))))
                    credentials = Credentials.new_from_json(json_encode(credentials))
                    user.update_credentials(credentials.to_json())
                    user.sync()
                else:
                    raise Exception('Token update failed')

            http_auth = credentials.authorize(httplib2.Http())
            drive_service = discovery.build('drive', 'v2', http_auth)



        else:
            print 'User not exists'
            return INT_NOTEXISTS
    except Exception as e:
        print 'Error occured in download ',e



def upload():
    pass

