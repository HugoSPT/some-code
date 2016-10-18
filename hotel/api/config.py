import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/hotel'
