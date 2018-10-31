import simplejson as json
import os
import datetime
import codecs
import numpy as np

class JsonRepository:
    @staticmethod
    def save(entity, file_path):
        j = json.dumps(entity, default=JsonRepository.datetime_handler, indent=4)
        with open(file_path, 'w') as f:
            f.write(j)

    @staticmethod
    def load(file_path):
        result = None
        if not os.path.exists(file_path):
            return result
        with codecs.open(file_path, "rb", "utf-8") as f:
            result = json.load(f)
        return result

    @staticmethod
    def datetime_handler(x):
        return x.isoformat() if hasattr(x, 'isoformat') else x