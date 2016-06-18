from mongoengine import connect
from config import config

connect(settings.APPLICATION_MONGODB_DBNAME, host=settings.APPLICATION_MONGODB_URI)