import logging
import httplib2
from dateutil import parser
from datetime import datetime, timedelta
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import Credentials
from googleapiclient.discovery import build
from apiclient import errors, http
from common.globalconst import *
from common.globalfunct import *
from server.errorhandler import *
from server.server_common import *
from database import *
from database.domain.user import User
from server.httpcomm.interface import *
import io
from apiclient import discovery
from oauth2client import client


parent_id = '0Bxu5-_bls171X3ZXZnVPbnhmVUE'
user = engine.query(User).filter(userId='116397074182558488295').first()
user_dict = user.__dict__
credentials = Credentials.new_from_json(user_dict['credentials'])
file_id = '0Bxu5-_bls171NzhWMVlOSV93YzA'
http_auth = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v2', http_auth)

def download_file(file_id,  filename='myfile'):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename, 'wb')
    downloader = http.MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print "Download %d%%." % int(status.progress() * 100)

#download_file(file_id=file_id)

def insert_file(service, title, description, parent_id, mime_type, filename):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  media_body = http.MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  body = {
    'title': title,
    'description': description,
    'mimeType': mime_type
  }
  # Set the parent folder.
  if parent_id:
    body['parents'] = [{'id': parent_id}]

  try:
    file = service.files().insert(
        body=body,
        media_body=media_body).execute()

    # Uncomment the following line to print the File ID
    print 'File ID: %s' % file['id']

    return file
  except errors.HttpError, error:
    print 'An error occured: %s' % error
    return None

file = 'C:\\Users\\shivankurkapoor\\GitHub\\BioinformaticsPipeline\\application\\test\\test.fastq'
insert_file(drive_service, title='test.fastq', description='test google drive upload api',parent_id=parent_id, mime_type=MIME_TYPE, filename=file)
