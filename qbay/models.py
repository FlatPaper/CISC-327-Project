from qbay import app
from flask_sqlalchemy import SQLAlchemy

import datetime
import enum


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
    user_balance = db.Column(db.Integer, nullable=False)
    listings = db.relationship('Listing', backref='user')
    reviews = db.relationship('Review', backref='user')
    transaction = db.relationship('Transaction', backref='user')


class Listing(db.Model):
    """
    An Object to Express a property listing.\n

    Properties:\n
    listing_id -- The integer ID for the listing\n
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
    reviews = db.relationship('Review', backref='listing', lazy=True)
    picture = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    transactions = db.relationship('Transaction', backref='listing')


class ReviewStarsEnum(enum.IntEnum):
    none = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class Review(db.Model):
    """
    A review model such that Users can leave reviews on listings.

    review_id -- id for the review model, the primary_key
    user_id -- the id of the user posting this review
    text -- the text of the review
    stars -- star rating of the review
    time -- time the review was posted
    listing -- the listing this review was posted on
    """
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    text = db.Column(db.String(2000), nullable=False)
    stars = db.Column(db.Enum(ReviewStarsEnum), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    listing = db.Column(db.Integer, db.ForeignKey('listings.listing_id'))


class Transaction(db.Model):
    """
        A Transaction object represents a succcessful transaction to rent a
        property listing.

        Includes the following properties:

        listing_id: Numeric ID of the property being rented
        user_id: Numeric ID of the user renting the property
        price: The price the listing was rented for
        user_balance: The amount of money the user has
                      remaining after the transaction
        transac_time: The time at which the transaction occurred
        trans_id: Numeric ID of the processed transaction
        currency: The currency the user used to pay qB&B
    """

    __tablename__ = 'transactions'

    listing_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    price = db.Column(db.Integer, nullable=False)
    user_balance = db.Column(db.Integer, db.ForeignKey('users.user_balance'))
    transaction_time = db.Column(db.DateTime,
                                 default=datetime.datetime.utcnow())
    transaction_id = db.Column(db.Integer, unique=True, nullable=True)
    currency = db.Column(db.String(100), nullable=False)


db.create_all()
