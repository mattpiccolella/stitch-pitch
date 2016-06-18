import os

class Config(object):
    APP_MONGODB_DBNAME = os.environ.get('APP_MONGODB_DBNAME', 'soundtrack')
    APP_MONGODB_USER = os.environ.get('APP_MONGODB_USER', 'root')
    APP_MONGODB_PASS = os.environ.get('APP_MONGODB_PASS', 'cranberry')
    APP_MONGODB_PORT = os.environ.get('APP_MONGODB_PORT', '27017')
    APP_MONGODB_HOST = os.environ.get('APP_MONGODB_HOST', 'localhost')
    APP_MONGODB_URI = os.environ.get('APP_MONGODB_URI', "mongodb://%s:%s/%s" %
                                            (APP_MONGODB_HOST, APP_MONGODB_PORT, APP_MONGODB_DBNAME))

config = Config()