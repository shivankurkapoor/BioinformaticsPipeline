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
from server.filehandler import *


def download(request_id=''):
    try:
        assert request_id
    except AssertionError:
        print 'Request Id is missing'
        return INT_ERROR_GENERAL
    try:
        request = engine.query(Request).filter(requestId=request_id)
        if request:
            request_dict = request.__dict__
            user_id = request_dict['userId']
            user = engine.query(Request).filter(userId=user_id)
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
                forward_file_id = request_dict['forward_file_id']
                backward_file_id = request_dict['backward_file_id']
                forward_file_name = FORWARD_FILE.format(request_id=request_id)
                backward_file_name = BACKWARD_FILE.format(request_id=request_id)
                forward_file_download_status_code = False
                backward_file_download_status_code = False
                if not request_dict['is_forward_file_downloaded']:
                    forward_file_download_status_code = download_file(user_id, drive_service, forward_file_id,
                                                                      forward_file_name)
                if not request_dict['is_backward_file_downloaded']:
                    backward_file_download_status_code = download_file(user_id, drive_service, backward_file_id,
                                                                       backward_file_name)

                if forward_file_download_status_code == INT_DOWNLOADED and backward_file_download_status_code == INT_DOWNLOADED:
                    print 'Files downloaded successfully'
                    request.set_is_backward_file_downloaded(True)
                    request.set_is_forward_file_downloaded(True)
                    request.sync()
                    return INT_OK
                elif forward_file_download_status_code == INT_DOWNLOADED:
                    print 'Backward file download failed'
                    request.set_is_backward_file_downloaded(True)
                    request.sync()
                    return INT_FAILURE_DOWNLOAD
                else:
                    print 'Forward file download failed'
                    request.set_is_forward_file_downloaded(True)
                    request.sync()
                    return INT_FAILURE_DOWNLOAD

            else:
                print 'User Id does not exists'
                return INT_NOTEXISTS

        else:
            print 'Request Id does not exists'
            return INT_NOTEXISTS
    except Exception as e:
        print 'Error occurred in download ', e
        return INT_FAILURE_DOWNLOAD


def upload(request_id=''):
    try:
        assert request_id
    except AssertionError:
        print 'Request Id is missing'
        return INT_ERROR_GENERAL

    try:
        request = engine.query(Request).filter(requestId=request_id)
        if request:
            request_dict = request.__dict__
            user_id = request_dict['userId']
            user = engine.query(Request).filter(userId=user_id)
            if request_dict['isprocessed']:
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
                    if request_dict['forward_file_parent_id']:
                        processed_file_parent_id = request_dict['forward_file_parent_id']
                    else:
                        processed_file_parent_id = request_dict['backward_file_parent_id']
                    title = RESULT_FILE.format(request_id)
                    description = DESCRIPTION
                    mime_type = MIME_TYPE
                    filename = DOWNLOAD_FILE_PATH.format(user_id=user_id) + "//" + title
                    upload_status, file_id = upload_file(drive_service, title, description, processed_file_parent_id,
                                                         mime_type, filename)
                    if upload_status == INT_UPLOADED:
                        request.set_processed_file_id(file_id)
                        request.set_isuploaded(True)
                        return INT_OK
                    else:
                        print 'File upload failed'
                        return upload_status

                else:
                    print 'User Id does not exists'
                    return INT_NOTEXISTS
            else:
                print 'Request not processed'
                return INT_ERROR_GENERAL
        else:
            print 'Request Id does not exists'
            return INT_NOTEXISTS

    except Exception as e:
        print 'Error occurred in download ', e
        return INT_FAILURE_DOWNLOAD
