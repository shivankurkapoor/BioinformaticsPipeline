from dynamo3 import DynamoDBConnection
from auth.auth_main import *
from database.domain.user import User
from database import *


engine.register(User)
engine.create_schema()
