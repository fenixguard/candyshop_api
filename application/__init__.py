
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://candyshop:qqqqqq@localhost:5432/candy_delivery"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config['REMEMBER_COOKIE_HTTPONLY'] = True


db = SQLAlchemy(app)

from application.model import *

app.secret_key = 'some_random_key'

from application.apis import api

app.register_blueprint(api)

db.create_all()
