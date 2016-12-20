import json
from datetime import datetime
from flask import jsonify

def json_encode(json_dict=None):
    assert isinstance(json_dict, dict)
    return json.dumps(json_dict)

def json_encode_flask(json_dict=None):
    assert isinstance(json_dict, dict)
    return jsonify(json_dict)

def json_decode(json_str=None):
    assert isinstance(json_str, str)
    return json.loads(json_str)

def datetime_util(date = None):
    '''
    This function converts the datetime format {YYYY-MM-DD HH:MM:SS}
    to {YYYY-MM-DDTHH:MM:SSZ} format. This date format is used by Google
    APIs
    :param date:
    :return:
    '''
    assert isinstance(date, datetime)
    dtstr = str(date)
    dtstr = dtstr.split('.')[0]
    date, time = dtstr.split(' ')
    return date+'T'+time+'Z'

