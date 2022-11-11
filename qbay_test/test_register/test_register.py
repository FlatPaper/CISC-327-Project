import string
from os import popen
from pathlib import Path
import subprocess
import random
from qbay.validators import validate_email, validate_password, \
    validate_username

# get expected input/output folder
current_folder = Path(__file__).parent


def test_register():
    """
    Let's test first by **input partition method** based on:
    Empty email | non RFC email
    empty username | username length < 2 | username length > 20 |
    username contains special characters | username has space in prefix
    empty password | password length < 6 | password has no uppercase |
    password has no lowercase | password has no special characters |
    good account
    """
    for i in range(1, 14):
        str_in = "input_partition/test_register" + str(i) + ".in"
        str_out = "input_partition/test_register" + str(i) + ".out"
        expected_in = open(current_folder.joinpath(str_in))
        expected_out = open(current_folder.joinpath(str_out)).read()

        # print("\n\nEXPECTED OUTPUT")
        # print(expected_out)
        # print("\n\n")

        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()
        #
        # print('---------------------------')
        # print('outputs',output)
        # print('---------------------------')

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()

