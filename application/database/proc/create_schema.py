from dynamo3 import DynamoDBConnection
from auth.auth_main import *
from database.domain.user import User
from database.domain.request import Request
from database import *


engine.register(User,Request)
engine.create_schema()
