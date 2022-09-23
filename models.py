import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Listing(db.Model):
    """An Object to Express a property listing.\n

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
    dscrpt = db.Column(db.String(500))
    rating = db.Column(db.Integer)
    reviews = db.relationship('Review', backref = 'reviews', lazy = True)
    picture = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    