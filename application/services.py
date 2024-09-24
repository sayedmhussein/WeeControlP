import datetime
import uuid


def get_uuid():
    return str(uuid.uuid4())

def get_now_ts():
    return str(datetime.datetime.now(datetime.UTC))
