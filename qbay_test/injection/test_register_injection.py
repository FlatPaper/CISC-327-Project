from qbay.models import register
from pathlib import Path


current_folder = Path(__file__).parent


def test_register_username():
    f = open(current_folder.joinpath('injection.txt'), 'r')
    lines = f.readlines()
    f.close
    # Go through each line of the general injection payload file
    # and insert each one as a paramater (in this case as username).
    # All other paramaters are valid.
    for line in lines:
        register(username=line,
                 email="validemail@gmail.com",
                 password="@Pass_pwd")


def test_register_email():
    f = open(current_folder.joinpath('injection.txt'), 'r')
    lines = f.readlines()
    f.close
    for line in lines:
        register(username="validusername",
                 email=line,
                 password="@Pass_pwd")


def test_register_password():
    f = open(current_folder.joinpath('injection.txt'), 'r')
    lines = f.readlines()
    f.close
    for line in lines:
        register(username="validusername",
                 email="validemail@gmail.com",
                 password=line)
