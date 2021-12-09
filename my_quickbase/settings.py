import os
import decouple
from my_quickbase import logger


try:
    Q_USER_TOKEN = os.environ['Q_USER_TOKEN']
    Q_REALM = os.environ['Q_REALM']

except KeyError:
    try:
        Q_USER_TOKEN = decouple.config('Q_USER_TOKEN')
        Q_REALM = decouple.config('Q_REALM')
    except decouple.UndefinedValueError:
        Q_USER_TOKEN = None
        Q_REALM = None
        logger.warning("No User Token or Realm environment variables found")