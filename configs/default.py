
import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEVELOPMENT').upper()
DEBUG = ENVIRONMENT == 'DEVELOPMENT'
TIMEZONE = 'US/Eastern'

# MONGODB
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017')
MONGO_DB = os.getenv('MONGO_DB', 'database')
