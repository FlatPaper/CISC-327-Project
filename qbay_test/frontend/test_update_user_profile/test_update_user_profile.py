from pathlib import Path
import subprocess
from qbay.models import User
from flask_sqlalchemy import SQLAlchemy
from qbay import app

# get expected input/output file
current_folder = Path(__file__).parent

db = SQLAlchemy(app)


def test_update_user_profile1():
    """
    First testing method is output partitioning based on:
    1. All valid inputs | 2. Invalid updated username (space at front) |
    3. Alphanumeric-only username | 4. Username must be between 2 and
    20 characters | 5. Invalid updated username (space at end) |
    6. Username already exists | 7. Special character in postal code |
    8. Postal code cannot be empty
    """
    for i in range(1, 9):
        db.session.query(User).delete()
        db.session.commit()
        str_in = "test_update_user_profile" + str(i) + ".in"
        str_out = "test_update_user_profile" + str(i) + ".out"
        expected_in = open(current_folder.joinpath(str_in))
        expected_out = open(current_folder.joinpath(str_out)).read()
        output = subprocess.run(['python', '-m', 'qbay'], stdin=expected_in,
                                capture_output=True,).stdout.decode()

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()


def test_update_user_profile2():
    """
    Second testing method is input partitioning based on:
    9. All valid inputs | 10. Non-valid username | 11. Non-valid email |
    12. Non-valid postal code
    """
    for i in range(9, 13):
        db.session.query(User).delete()
        db.session.commit()
        str_in = "test_update_user_profile" + str(i) + ".in"
        str_out = "test_update_user_profile" + str(i) + ".out"
        expected_in = open(current_folder.joinpath(str_in))
        expected_out = open(current_folder.joinpath(str_out)).read()
        output = subprocess.run(['python', '-m', 'qbay'], stdin=expected_in,
                                capture_output=True,).stdout.decode()

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()


def test_update_user_profile3():
    """
    Third testing method is boundry testing based on:
    13. Check upper bound of username | 14. Check lower bound of username
    Upper bound: username should be less than 20 characters, tests to see if
    2000 characters can be handled.
    Lower bound: username should be more than 2 characters, tests to see if
    0 characters can be handled.
    """
    for i in range(13, 15):
        db.session.query(User).delete()
        db.session.commit()
        str_in = "test_update_user_profile" + str(i) + ".in"
        str_out = "test_update_user_profile" + str(i) + ".out"
        expected_in = open(current_folder.joinpath(str_in))
        expected_out = open(current_folder.joinpath(str_out)).read()
        output = subprocess.run(['python', '-m', 'qbay'], stdin=expected_in,
                                capture_output=True,).stdout.decode()

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()
