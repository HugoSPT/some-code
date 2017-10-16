from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
db = SQLAlchemy(app)

import api.hotels.controllers

app.config.from_object('config')
