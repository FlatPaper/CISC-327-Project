from pathlib import Path
import subprocess
from qbay.models import User, register
from qbay import app
from flask_sqlalchemy import SQLAlchemy

# get expected input/output folder
current_folder = Path(__file__).parent

db = SQLAlchemy(app)


def test_login1():
    """
    Input partition test
    Empty email | non RFC email
    empty password | password length < 6 | password has no uppercase |
    password has no lowercase | password has no special characters |
    existing account
    """

    db.session.query(User).delete()
    db.session.commit()
    register(username="FlatPaper", email="good.email@gmail.com",
             password="GoodPassword!")

    for i in range(1, 9):
        str_in = "test_cases/test_login" + str(i) + ".in"
        str_out = "test_cases/test_login" + str(i) + ".out"
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


def test_login2():
    """
    Output partition test
    Login failed and login succeeded
    """

    for i in range(9, 11):
        str_in = "test_cases/test_login" + str(i) + ".in"
        str_out = "test_cases/test_login" + str(i) + ".out"
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


def test_login3():
    """
    Boundary Value Robustness Testing
    Put a limit on email and password lengths: Will it crash?
    past 2000 characters each?
    Should pass constraints with failure.
    """
    # Code to output big boundary test on username and password
    # fin = open("test_cases/test_login11.in", "w")
    # fin.write("1\n")
    # email = "a" * 2000 + "@gmail.com"
    # password = "G00dPassword!" * 154
    # fin.write(email + '\n')
    # fin.write(password + '\n')
    # fin.close()

    str_in = "test_cases/test_login11.in"
    str_out = "test_cases/test_login11.out"
    expected_in = open(current_folder.joinpath(str_in))
    expected_out = open(current_folder.joinpath(str_out)).read()

    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()

    expected_out = expected_out.replace('\r', '')
    output = output.replace('\r', '')
    expected_out = expected_out.replace('\n', '')
    output = output.replace('\n', '')
    expected_out = expected_out.replace(' ', '')
    output = output.replace(' ', '')

    assert output.strip() == expected_out.strip()
