from pathlib import Path
import subprocess
from qbay.models import User, register
from flask_sqlalchemy import SQLAlchemy
from qbay import app

db = SQLAlchemy(app)


def test_create_listing_input_partition():
    """
    Test 1 All valid inputs for create listing
    Test 2 Non Valid title
    Test 3 Non valid description
    Test 4 Non Valid Price
    """
    current_folder = Path(__file__).parent

    db.session.query(User).delete()
    db.session.commit()

    register(email="pass_empty@gmail.com", password="Pass_pwd",
             username="david")
    
    for i in range(1, 5):
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


def test_create_listing_output_exhaustive():
    """
    Test 5 All valid inputs for create listing
    Test 6 Title is not alphanumeric
    Test 7 Title is greater than 80 characters
    Test 8 Title has spaces at the end and start
    Test 9 Description not between 20-2000 characters.
    test 10 Description not longer than the title.
    Test 11 Price is not a number
    Test 12 Price is not between 10-10000
    test 13 Shares title with another listing
    """
    current_folder = Path(__file__).parent
    for i in range(5, 14):
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


def test_create_listing_input_boundary():
    """
    Test 14 All valid inputs for create listing
    Test 15 Title is 80 characters
    Test 16 Description is 20 charcters
    Test 17 Description is 2000 chracters
    Test 18 Title and Description are the same length
    Test 19 Price is 10
    Test 20 Price is 10000
    """
    current_folder = Path(__file__).parent
    for i in range(14, 21):
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
    