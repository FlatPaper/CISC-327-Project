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
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    billing_address = db.Column(db.String, nullable=True)
    postal_code = db.Column(db.String, nullable=True)
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
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    last_modified_date = db.Column(db.DateTime)
    address = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # 'user' property defined in User.listings via backref
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
    text = db.Column(db.String, nullable=False)
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


def validate_email(email: str):
    # Check for empty email field
    if len(email) == 0:
        return False, "Email cannot be empty."

    # Check that email matches RFC 5322 constraints with a very long regex
    if not EMAIL_REGEX.match(email):
        return False, "Email does not follow addr-spec defined in RFC 5322."

    return True, "Email is in the correct format."


def validate_password(password: str):
    # Check for empty email and password fields
    if len(password) == 0:
        return False, "Password cannot be empty."

    # Check for password complexity constraints
    if len(password) < 6:
        return False, "Password is too short."
    if not any(ch.isupper() for ch in password):
        return False, "The password does not contain any uppercase characters."
    if not any(ch.islower() for ch in password):
        return False, "The password does not contain any lowercase characters."
    if not any(not ch.isalnum() for ch in password):
        return False, "The password does not contain any special characters."

    return True, "Password meets the constraints."


def validate_username(username: str):
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

    return True, "Username meets the constraints."


def register(username: str, email: str, password: str):
    # Validate the email constraints
    flag, msg = validate_email(email)
    if flag is False:
        return flag, msg

    # Validate the password constraints
    flag, msg = validate_password(password)
    if flag is False:
        return flag, msg

    # Check for username constraints
    flag, msg = validate_username(username)
    if flag is False:
        return flag, msg

    # Check if email has been used
    email_query = User.query.filter_by(email=email).all()
    if len(email_query) > 0:
        return False, "This email has been used already."

    user = User(username=username, email=email, password=password,
                balance=100)

    db.session.add(user)

    db.session.commit()

    return True, "User has been created!"


def login(email: str, password: str):
    # Validate email constraints
    flag, msg = validate_email(email)
    if flag is False:
        return flag, msg

    # Validate password constraints
    flag, msg = validate_password(password)
    if flag is False:
        return flag, msg

    match_accounts = User.query.filter_by(email=email, password=password).all()
    if len(match_accounts) < 1:
        return None, "This account does not exist"
    # Check for an "impossible" situation for debugging purposes in the future
    if len(match_accounts) > 1:
        return None, "There are more than one accounts with this email!"

    return match_accounts[0], "This account exists."


def create_listing(title: str, description: str, price: int,
                   address: str, user_id: int):
    if any(not x.isalnum() or not x.isspace() for x in title):
        return False, "The title of the listing must be alphanumeric."
    if title[0] == " " or title[-1] == " ":
        return False, "Space is allowed if it's not a prefix or suffix."
    if len(title) > 80:
        return False, "Length of title must be 80 or less characters."
    if len(description < 20) or len(description > 2000):
        return False, "Description length must be between 20-2000 characters."
    if len(description) <= len(title):
        return False, "Description length must be longer than the title."
    if price < 10 or price > 10000:
        return False, "Price must be between [10, 10000]."

    date = datetime.today()

    user = User.query.get(user_id)
    if user is None:
        return False, "User id does not exist!"
    user_email = user.email

    listings = User.query.get(user_id).listings
    if any(title == product.title for product in listings):
        return False, "Listings cannot have the same title."

    listing_obj = Listing(title=title, description=description,
                          price=price, last_modified_date=date,
                          address=address, user_id=user_id,
                          user_email=user_email)

    db.session.add(listing_obj)

    db.session.commit()

    return True


def validate_title(title: str):
    if not title.isalnum():
        return False, "Title of the product must be alphanumeric."

    if len(title) > 80:
        return False, "Title of the product must be 80 characters or less."

    if title != title.strip():
        return False, "Spaces as prefixes and suffixes are not allowed."

    return True, "Title meets constraints."


def validate_description(description: str, title: str):
    if 20 > len(description) > 2000:
        return False, "Description length must be between 20-2000 characters."

    if len(description) < len(title):
        return False, "Description must be longer than the title."

    return True, "Description meets constraints."


def validate_price(price: int, listing):
    if 10 > price > 1000:
        return False, "Price must be between 10 and 1000."

    if price <= listing.price:
        return False, "New price must be greater than the previous price."

    return True, "Price meets constraints."


def validate_address(address: str):
    if not address.isalnum():
        return False, "Address must be alphanumeric."

    return True, "Address meets constraints."


def validate_date(date: datetime):
    low = date(2021, 1, 2)
    high = date(2025, 1, 2)
    if low > date > high:
        return False, "New date must be between 2021-01-02 and 2025-01-02."

    return True, "Date was modified."


def update_listing(listing_id: int, title=None,
                   description=None, price=None, address=None):
    """
        This function updates the attributes of the posted listing.
        If any of the inputs are not given, then automatically assigns them
        None and updates the remaining attributes.
        If none are given, no attributes are updated.
    """
    listing = Listing.query.get(listing_id)

    # Each None ensures that if a missing input variable does not change.
    if title is not None:
        # Validate title constraints
        flag, msg = validate_title(title)
        if flag is False:
            return flag, msg
        else:
            listing.title = title

    if description is not None:
        # Validate description constraints
        flag, msg = validate_description(description, listing.title)
        if flag is False:
            return flag, msg
        else:
            listing.description = description

    if price is not None:
        # Validate price constraints
        flag, msg = validate_price(price, listing)
        if flag is False:
            return flag, msg
        else:
            listing.price = price

    if address is not None:
        # Validate address constraints
        flag, msg = validate_address(address)
        if flag is False:
            return flag, msg
        else:
            listing.address = address

    # Validate date constraints
    flag, msg = validate_date(datetime.today())
    if flag is False:
        return flag, msg
    else:
        listing.last_date_modified = datetime.today()

    return True, "Listing has been updated."
