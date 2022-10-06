from qbay import app
from flask_sqlalchemy import SQLAlchemy

import datetime
import enum
import re


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
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    billing_address = db.Column(db.String(120), nullable=True)
    postal_code = db.Column(db.String(7), nullable=True)
    balance = db.Column(db.Integer, nullable=False)
    listings = db.relationship('Listing', backref='user')
    reviews = db.relationship('Review', backref='user')
    bookings = db.relationship('Booking', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)


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
    # 'user' property defined in User.listings via backref
    price = db.Column(db.Integer)
    reviews = db.relationship('Review', backref='listing')
    bookings = db.relationship('Booking', backref='listing')

    def __repr__(self):
        return '<Listing {}>'.format(self.listing_id)


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # 'user' property defined in User.listings via backref
    text = db.Column(db.String(2000), nullable=False)
    stars = db.Column(db.Enum(ReviewStarsEnum), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'))
    # 'listing' property defined in Listing.reviews via backref

    def __repr__(self):
        return '<Review {}>'.format(self.review_id)


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
    # 'user' property defined in User.listings via backref
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'))
    # 'listing' property defined in Listings.bookings via backref
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Booking {}>'.format(self.booking_id)


db.create_all()

EMAIL_REGEX = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.["
                         r"-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t "
                         r"-~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.["
                         r"-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")


def register(username: str, email: str, password: str):
    # Check for empty email and password fields
    if len(email) == 0:
        return False, "Email cannot be empty."
    if len(password) == 0:
        return False, "Password cannot be empty."

    # Check that email matches RFC 5322 constraints with a very long regex
    if not EMAIL_REGEX.match(email):
        return False, "Email does not follow addr-spec defined in RFC 5322/"

    # Check for password complexity constraints
    if len(password) < 6:
        return False, "Password is too short."
    if not any(ch.isupper() for ch in password):
        return False, "The password does not contain any uppercase characters."
    if not any(ch.islower() for ch in password):
        return False, "The password does not contain any lowercase characters."
    if not any(not ch.isalnum() for ch in password):
        return False, "The password does not contain any special characters."

    # Check for username constraints
    if len(username) == 0:
        return False, "The username is empty."
    if len(username) <= 2 or len(username) >= 20:
        error_info = "The username must be longer than 2 characters and " \
                     "shorter than 20 characters. "
        return False, error_info
    if not all(ch.isalnum() or ch.isspace() for ch in username):
        error_info = "The username contains characters that are not " \
                     "alphanumeric or a space. "
        return False, error_info
    if username[0] == ' ':
        return False, "The username cannot contain a space as its prefix."
    if username[len(username) - 1] == ' ':
        return False, "The username cannot contain a space as its suffix."

    # Check if email has been used
    email_query = User.query.filter_by(email=email).all()
    if len(email_query) > 0:
        return False, "This email has been used already."

    user = User(username=username, email=email, password=password,
                balance=100)

    db.session.add(user)

    db.session.commit()

    return True, "User has been created!"
