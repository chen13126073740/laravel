import json
import os


class Config:
    config = {}

    @classmethod
    def init(cls):
        files = os.listdir('./config/')
        for file in files:
            print(file)
            with open('./config/' + file, 'r') as f:
                res = f.read()
                config = json.loads(res)
            cls.config[file.replace('.json', '')] = config


    @classmethod
    def get(cls, names):
        names = names.split('.')
        config = cls.config
        for name in names:
            config = config[name]
        return config
