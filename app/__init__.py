##from flask import Flask
##from flask_sqlalchemy import SQLAlchemy
###from flask_admin import Admin
###from flask_contrib.sqla import ModelView
##
##app = Flask(__name__)
##@app.route('/')
##@app.index('/index')
##def index():
##    return 'Hello!'
##
##user_db = SQLAlchemy(app)
##
##class User(user_db.Model):
##    identification = user_db.Column(user_db.Integer, primary_key=True)
##    name = user_db.Column(user_db.String(32), unique=True)
##    email = user_db.Column(user_db.String(32), unique=True)
##
##if __name__ == '__main__':
##    admin = Admin(app)
##    #admin.add_view(ModelView(User, user_db.session))
##
##    db.create_all()
##    app.run()
from flask import Flask, request
##import dateutil.parser as parser
##import geopy as geo

app = Flask(__name__)

from app import routes
