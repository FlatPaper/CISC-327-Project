from qbay.models import *
from qbay.cli import register_page


def user_logged_in():
    selection = input(
        "Your options are as follows:"
        "Please press 1 to create a listing."
        "Please press 2 to update a listing."
        "Please press 3 to update your user profile page."
    )


def main():
    while True:
        logged_in = False
        if logged_in:
            selection = input(
                "Your options are as follows:"
                "Please press 1 to create a listing."
                "Please press 2 to update a listing."
                "Please press 3 to update your user profile page."
                "Please press 4 to log out."
            )
            selection = selection.strip()
        else:
            selection = input(
                "Your options are as follows:\n"
                "Please press 1 to log in.\n"
                "Please press 2 to register an account.\n"
                "Please press 3 to exit.\n"
            )
            selection = selection.strip()
            if selection == "2":
                register_page()


if __name__ == '__main__':
    main()