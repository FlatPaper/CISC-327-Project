import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Transaction(db.Model):

    """
        A Transaction object represents a succcessful transaction to rent a property listing.

        Includes the following properties:

        listing_id: Numeric ID of the property being rented
        user_id: Numeric ID of the user renting the property
        price: The price the listing was rented for
        user_balance: The amount of money the user has remaining after the transaction
        transac_time: The time at which the transaction occurred
        trans_id: Numeric ID of the processed transaction
        currency: The currency the user used to pay qB&B
    """

    __tablename__ = 'transactions'

    listing_id = db.Column(db.Integer, primary_key = true)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    price = db.Column(db.Integer, nullable = False)
    user_balance = db.Column(db.Integer, 'users.user_balance')
    trans_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    trans_id = db.Column(db.Integer, unique = True, nullable = True)
    currency = db.Column(db.string(100), nullable = False)
