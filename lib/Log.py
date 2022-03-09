import os
import json
import datetime
import time


class Log:
    log_file = './data/log/fail.log'

    @classmethod
    def debug(cls, obj):
        if isinstance(obj, (object, list)):
            obj = json.dumps(obj, sort_keys=True, ensure_ascii=True, indent=2, separators=(',', ': '))
        with open(cls.log_file, 'a') as f:
            f.write("#" + str(datetime.datetime.now()) + "(" + str(time.time()) + ')\n')
            f.write(obj + '\n')

    @classmethod
    def remove(cls):
        if os.path.exists(Log.log_file):
            os.remove(cls.log_file)

    @classmethod
    def clean(cls):
        with open(cls.log_file, 'w') as f:
            f.write('')
