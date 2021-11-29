import os
import decouple

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
        print("No User Token or Realm environment variables found")  # TODO convert to logging
