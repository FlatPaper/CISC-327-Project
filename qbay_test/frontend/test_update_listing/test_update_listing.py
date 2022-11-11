from os import popen
from pathlib import Path
import subprocess
from qbay.models import register, create_listing, User, Listing
from flask_sqlalchemy import SQLAlchemy
from qbay import app

# get expected input/output file
current_folder = Path(__file__).parent

db = SQLAlchemy(app)


def test_update_listing1():
    """
    Input partition method.
    Split inputs by:
    Title not being alphanumeric
    Title being > 80 characters
    Title have prefix / suffix as space
    Description being < 20 characters or > 2000 characters
    Description being shorter than the title
    Price being < 10 or > 1000
    Price being < previous price
    vs. Good input
    """

    db.session.query(User).delete()
    db.session.query(Listing).delete()
    db.session.commit()

    register(username="Temporary 1", email="pass_empty@gmail.com",
             password="Pass_pwd")
    create_listing(title="Test Title1", description="Temporary description",
                   price=50, address="", user_id=1)

    for i in range(1, 9):
        # read expected in/out
        expected_in = open(current_folder.joinpath(
            'test_update_listing_' + str(i) + '.in'))
        expected_out = open(current_folder.joinpath(
            'test_update_listing_' + str(i) + '.out')).read()

        # print(expected_out)

        # pip the input
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()

        # print('outputs', output)

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()


def test_update_listing2():
    """
    Output partition method
    Should fail updating a listing vs. succeeding updating
    """

    for i in range(1, 9):
        # read expected in/out
        expected_in = open(current_folder.joinpath(
            'test_update_listing_' + str(i) + '.in'))
        expected_out = open(current_folder.joinpath(
            'test_update_listing_' + str(i) + '.out')).read()

        # print(expected_out)

        # pip the input
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()

        # print('outputs', output)

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()
