import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    # An object to display a user entity
    """
    languages -- A list of languages the user speaks
    listings -- A list of listings the user has 
    pfp -- A profile picture on the user's profile
    """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_num = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(2000), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    response_rate = db.Column(db.Integer, nullable=False)
    listings = db.relationship('Listing', backref='users')
    
    
class Listing(db.Model):
    """
    An Object to Express a property listing.\n

    Properties:\n
    listing_id-- The integer ID for the listing\n
    address   -- A String in the form country,province,city,street,number \n
    user_id   -- The user who that made the listing\n
    price   -- A float, price per night of the property\n
    dscrpt  -- A string describing the property\n
    rating  -- A float between 0-5
    pics    -- A list of image files of the property\n
    aval    -- A list of pairs of days
    reviews -- A list of "Review" objects\n
    """

    __tablename__ = 'listings'

    listing_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    price = db.Column(db.Integer)
    description = db.Column(db.String(500))
    rating = db.Column(db.Integer)
    reviews = db.relationship('Review', backref='reviews', lazy=True)
    picture = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    