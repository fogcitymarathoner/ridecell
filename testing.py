from datetime import datetime as dt
from datetime import timedelta as td
import pytz
import random
import string

epoch = dt(year=1970, month=1, day=1, hour=0, minute=0, tzinfo=pytz.UTC)


def random_string(N):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

