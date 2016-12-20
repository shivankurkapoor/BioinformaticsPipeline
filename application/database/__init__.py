from dynamo3 import DynamoDBConnection
from flywheel import Engine
from auth.auth_main import *


connection = DynamoDBConnection.connect(region=DynamoAuth.region,
                                        access_key=DynamoAuth.access_key,
                                        secret_key=DynamoAuth.secret_key,
                                        host="localhost",
                                        port=8000,
                                        is_secure=False
                                        )

engine = Engine(connection)
