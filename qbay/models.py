from qbay import app
from flask_sqlalchemy import SQLAlchemy

import datetime
import enum


db = SQLAlchemy(app)


class User(db.Model):
    # An object to display a user entity
    """
    user_id: id of the user (unique)
    email: a string that respresents the users email
    password: the users password
    billing_address: billing address of the user
    postal_code: postal code of the user
    balance: balance of the user
    listings: all listings the user owns
    reviews: all reviews posted by the user
    bookings: all bookings related to the user
    """
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    billing_address = db.Column(db.String(120), nullable=False)
    postal_code = db.Column(db.String(7), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    listings = db.relationship('Listing')
    reviews = db.relationship('Review')
    bookings = db.relationship('Booking')


class Listing(db.Model):
    """
    An Object to Express a property listing.\n

    Properties:\n
    listing_id: The integer ID for the listing\n
    title: title of the listing
    description: description of the listing
    price: price of the listing
    last_modified_date: last date the listing was modified
    address: A String in the form country,province,city,street,number
    user_id: The user who that made the listing
    price: A float, price per night of the property
    reviews: all the reviews linked to this listing
    bookings: all the bookings linked to this listing
    """
    __tablename__ = 'listings'

    listing_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    last_modified_date = db.Column(db.DateTime)
    address = db.Column(db.String(200), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    price = db.Column(db.Integer)
    reviews = db.relationship('Review')
    bookings = db.relationship('Booking')


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

    review_id: id for the review model, the primary_key
    user_id: the id of the user posting this review
    text: the text of the review
    star: star rating of the review
    date: time the review was posted
    listing: the listing this review was posted on
    """
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    text = db.Column(db.String(2000), nullable=False)
    stars = db.Column(db.Enum(ReviewStarsEnum), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    listing = db.Column(db.Integer, db.ForeignKey('listings.listing_id'))


class Booking(db.Model):
    """
        A Booking object represents a booking to rent a
        property listing.

        Includes the following properties:

        booking_id: Booking ID
        user_id: Numeric ID of the user renting the property
        listing_id: ID of the listing trying to be booked
        price: The price the listing was rented for
        date: The time at which the booking is posted
    """
    __tablename__ = 'transactions'

    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('reviews.review_id'))
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())


db.create_all()
