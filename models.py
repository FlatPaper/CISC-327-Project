from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    # An object to display a user entity
    
    '''
    languages -- A list of languages the user speaks
    listings -- A list of listings the user has 
    pfp -- A profile picture on the user's profile
    '''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_num = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(2000), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    response_rate = db.Column(db.Integer, nullable=False)
