'''
This is the main file for the backend server
'''

from flask import Flask, request, render_template
from server.errorhandler import *
from server.authentication import *
from common.globalconst import *
from common.globalfunct import *


application = Flask(__name__)


@application.route('/')
def app_demo():
  """
    This is the simple demo
    :return:
    """
  return render_template('index.html')

@application.route('/authenticate', methods=['POST'])
def app_authenticate():
    '''
    This API authenticates the user
    :return:
    '''
    auth_fields = json_decode(request.data)
    return authenticate_proc(auth_fields, request.remote_addr)


@application.errorhandler(404)
def page_not_found(error):
  """
    This is to process error http requests
    :param error:
    :return:
    """
  print '404 error, redirecting...'
  return '404 error, redirecting...'


@application.errorhandler(500)
def page_not_found(error):
  """
    This is to process error http requests
    :param error:
    :return:
    """
  print '500 Error. Server Internal Error...'
  return '500 Error. Server Internal Error...'


@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
  response = json_encode_flask(error.to_dict())
  response.status_code = error.status_code
  return response


# starter
if __name__ == '__main__':
    application.secret_key = APP_SECRET_KEY
    application.debug = True
    application.run(host='localhost',port=5000)
    # application.run(debug=True)


