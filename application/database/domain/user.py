from datetime import datetime
from flywheel.fields.types import DateTimeType
from flywheel import Model, Field, Engine,set_
from dynamo3 import (Binary, NUMBER, STRING, BINARY, NUMBER_SET, STRING_SET,
                     BINARY_SET, BOOL, MAP, LIST)
from types import BooleanType


class User(Model):
    userId = Field(data_type=STRING, hash_key=True)
    family_name = Field(data_type=STRING)
    given_name = Field(data_type=STRING)
    email = Field(data_type=STRING)
    gender = Field(data_type=STRING)
    link = Field(data_type=STRING)
    locale = Field(data_type=STRING)
    name = Field(data_type=STRING)
    picture = Field(data_type=STRING)
    verified_email = Field(data_type=BooleanType)
    credentials = Field(data_type=STRING)



    def __init__(self, userid='',credentials=''):
        super(User, self).__init__()
        self.userId = userid
        self.credentials=credentials


    def save_user_info(self, user_info):
        for key,value in user_info.items():
            if key != 'id' and value is not None:
                setattr(self, key, value)


    def update_credentials(self, credentials):
        setattr(self, 'credentials', credentials)


    user_attr = ['userId', 'family_name', 'given_name', 'email',
                 'gender', 'link', 'locale', 'name', 'picture',
                 'verified_email', 'credentials']