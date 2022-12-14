from pathlib import Path
import subprocess
from qbay.models import User, Listing, register, create_listing
from flask_sqlalchemy import SQLAlchemy
from qbay import app

db = SQLAlchemy(app)


def test_booking_input_partition():
    """
    Test 1 All valid inputs for booking
    Test 2 Book for a past day
    Test 3 Book listing user owns
    Test 4 less balance than needed
    Test 5 already booked
    """
    current_folder = Path(__file__).parent

    db.session.query(User).delete()
    db.session.query(Listing).delete()
    db.session.commit()

    register(email="booker@gmail.com", password="Pass_book1",
             username="booker")
    register(email="lister@gmail.com", password="Pass_list1",
             username="lister")
    create_listing(title="bookit", description="this should really get booked",
                   price=100, address="123book", user_id=2)
    create_listing(title="pricey", description="this is really too expensive",
                   price=500, address="124book", user_id=2)

    for i in range(1, 6):
        expected_in = open(current_folder.joinpath('test' + str(i) + '.in'))
        expected_out = open(current_folder.joinpath('test' + str(i)
                            + '.out')).read()
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()
        a = "".join(str(expected_out).split())
        b = "".join(str(output).split())
        assert a == b


def test_booking_output_exhaustive():
    """
    Test 6 Booking was created!
    Test 7 listing does not exist
    Test 8 A user cannot book a listing for his/her own listing.
    Test 9 The listing price is greater than your balance.
    Test 10 You cannot book a listing for today or any previous day!
    Test 11 This listing is already booked for the desired date.
    """
    
    current_folder = Path(__file__).parent

    db.session.query(User).delete()
    db.session.query(Listing).delete()
    db.session.commit()

    register(email="booker@gmail.com", password="Pass_book1",
             username="booker")
    register(email="lister@gmail.com", password="Pass_list1",
             username="lister")
    create_listing(title="bookit", description="this should really get booked",
                   price=100, address="123book", user_id=2)
    create_listing(title="pricey", description="this is really too expensive",
                   price=500, address="124book", user_id=2)

    for i in range(6, 12):
        expected_in = open(current_folder.joinpath('test' + str(i) + '.in'))
        expected_out = open(current_folder.joinpath('test' + str(i)
                            + '.out')).read()
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()
        a = "".join(str(expected_out).split())
        b = "".join(str(output).split())
        assert a == b


def test_booking_input_boundary():
    """
    Test 12 Have equal balance to booking price
    Test 13 Book a listing for one day after another booking
    """
    current_folder = Path(__file__).parent

    db.session.query(User).delete()
    db.session.query(Listing).delete()
    db.session.commit()

    register(email="booker@gmail.com", password="Pass_book1",
             username="booker")
    register(email="lister@gmail.com", password="Pass_list1",
             username="lister")
    create_listing(title="bookit", description="this should really get booked",
                   price=100, address="123book", user_id=2)
    create_listing(title="pricey", description="this is really too expensive",
                   price=500, address="124book", user_id=2)

    for i in range(12, 14):
        expected_in = open(current_folder.joinpath('test' + str(i) + '.in'))
        expected_out = open(current_folder.joinpath('test' + str(i)
                            + '.out')).read()
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()
        a = "".join(str(expected_out).split())
        b = "".join(str(output).split())
        assert a == b
