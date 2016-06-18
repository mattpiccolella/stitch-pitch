import os

class Config(object):
    APPLICATION_MONGODB_DBNAME = os.environ.get('APP_MONGODB_DBNAME', 'soundtrack')
    APPLICATION_MONGODB_USER = os.environ.get('APP_MONGODB_USER', '')
    APPLICATION_MONGODB_PASS = os.environ.get('APP_MONGODB_PASS', '')
    APPLICATION_MONGODB_PORT = os.environ.get('APP_MONGODB_PORT', '27017')
    APPLICATION_MONGODB_HOST = os.environ.get('APP_MONGODB_HOST', 'localhost')
    APPLICATION_MONGODB_URI = os.environ.get('APP_MONGODB_URI', "mongodb://%s:%s/%s" %
                                            (APPLICATION_MONGODB_HOST, APPLICATION_MONGODB_PORT, APPLICATION_MONGODB_DBNAME))

config = Config()