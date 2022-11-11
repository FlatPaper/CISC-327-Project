from os import popen
from pathlib import Path
import subprocess
from qbay.models import register

# get expected input/output file
current_folder = Path(__file__).parent


def test_login():
    """capsys -- object created by pytest to
    capture stdout and stderr"""

    register(username="Temporary 1", email="pass_empty@gmail.com",
             password="Pass_pwd")

    for i in range(1, 12):
        # read expected in/out
        expected_in = open(current_folder.joinpath(
            'test_update_listing_' + str(i) + '.in'))
        expected_out = open(current_folder.joinpath(
            'test_update_listing_' + str(i) + '.out')).read()

        print(expected_out)

        # pip the input
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()

        print('outputs', output)

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()
