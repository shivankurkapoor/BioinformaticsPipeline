from datetime import datetime
from flywheel.fields.types import DateTimeType
from flywheel import Model, Field, Engine, set_
from dynamo3 import (Binary, NUMBER, STRING, BINARY, NUMBER_SET, STRING_SET,
                     BINARY_SET, BOOL, MAP, LIST)
from types import BooleanType


class Request(Model):
    userId = Field(data_type=STRING, hash_key=True)
    forward_file_id = Field(data_type=STRING)
    backward_file_id = Field(data_type=STRING)
    forward_file_parent_id = Field(data_type=STRING)
    backward_file_parent_id = Field(data_type=STRING)
    time_create = Field(data_type=datetime)
    time_processed = Field(data_type=datetime)
    isprocessed = Field(data_type=BooleanType)
    processed_file = Field(data_type=STRING)
    processed_file_id = Field(data_type=STRING)
    processed_file_parent_id = Field(data_type=STRING)
    isuploaded = Field(data_type=BooleanType)
    forward_primer_seq = Field(data_type=STRING)
    backward_primer_seq = Field(data_type=STRING)
    percentage = Field(data_type=NUMBER)
    basecount = Field(data_type=NUMBER)
    collapse_length = Field(data_type=NUMBER)

    def __init__(self, collapse_length, userid='', forward_file_parent_id='', forward_file_id='', backward_file_id='',
                 backward_file_parent_id='', forward_primer_seq='', backward_primer_seq='', percentage=0, basecount=0):
        super(Request, self).__init__()
        self.userId = userid
        self.forward_file_id = forward_file_id
        self.backward_file_id = backward_file_id
        self.forward_file_parent_id = forward_file_parent_id
        self.backward_file_parent_id = backward_file_parent_id
        self.time_create = datetime.now()
        self.isprocessed = False
        self.isuploaded = False
        self.backward_primer_seq = backward_primer_seq
        self.forward_primer_seq = forward_primer_seq
        self.basecount = basecount
        self.collapse_length = collapse_length

    def set_processed_file(self, path):
        setattr(self, 'processed_file', path)

    def set_processed_file_id(self, id):
        setattr(self, 'processed_file_id', id)

    def set_time_processed(self, timestamp):
        setattr(self, 'time_processed', timestamp)

    def set_isprocessed(self, isprocesseed=False):
        setattr(self, 'isprocessed', isprocesseed)

    def set_isuploaded(self, isuploaded=False):
        setattr(self, 'isuploaded', isuploaded)

    def set_processed_file_parent_id(self, id):
        setattr(self, 'processed_file_parent_id', id)

    user_attr = ['userId', 'forward_file_id', 'backward_file_id',
                 'forward_parent_id', 'backward_parent_id', 'time_create', 'time_processed', 'isprocessed',
                 'processed_file', 'processed_file_id', 'isuploaded', 'forward_primer_seq',
                 'backward_primer_seq', 'percentage', 'basecount', 'collapse_length']
