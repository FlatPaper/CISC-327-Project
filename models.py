import datetime
import enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class ReviewStarsEnum(enum.IntEnum):
    none = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    text = db.Column(db.String(2000), nullable=False)
    stars = db.Column(db.Enum(ReviewStarsEnum), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    listing = db.Column(db.Integer, db.ForeignKey('listing.listing_id'))
