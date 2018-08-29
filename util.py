import time
from datetime import datetime

def date_to_unix(date):
    return int(time.mktime(date.timetuple()))