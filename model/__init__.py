from mongoengine import connect
from config import config

connect(config.APP_MONGODB_DBNAME, host=config.APP_MONGODB_URI)