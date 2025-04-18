from qbay.models import *
from qbay.cli import register_page, login_page, update_user_page, \
    create_listing_page, update_listing_page, book_listing_page


def main():
    logged_in = False
    current_user = None
    while True:
        if logged_in:
            selection = input(
                "Your options are as follows:\n"
                "Please press 1 to create a listing.\n"
                "Please press 2 to update a listing.\n"
                "Please press 3 to update your user profile page.\n"
                "Please press 4 to log out.\n"
            )
            selection = selection.strip()
            if selection == "1":
                user_email = current_user[0]
                user_id = User.query.filter_by(
                    email=user_email).all()[0].user_id
                create_listing_page(user_id)
            if selection == "2":
                user_email = current_user[0]
                user_id = User.query.filter_by(
                    email=user_email).all()[0].user_id
                flag, msg = update_listing_page(user_id)
                print(msg)
            if selection == "3":
                user = User.query.filter_by(email=current_user[0]).all()[0]
                result = update_user_page(user.user_id)
                if result[0]:
                    print("Successfully updated profile!")
                else:
                    print("Unable to update profile!")
                    print(result[1])
            if selection == "4":
                logged_in = False
                current_user = None
            if selection == "5":
                user_email = current_user[0]
                user_id = User.query.filter_by(
                    email=user_email).all()[0].user_id
                book_listing_page(user_id)
        else:
            selection = input(
                "Your options are as follows:\n"
                "Please press 1 to log in.\n"
                "Please press 2 to register an account.\n"
                "Please press 3 to exit.\n"
            )
            selection = selection.strip()
            if selection == "1":
                result = login_page()
                if result[0]:
                    # Stores tuple of (email, password)
                    current_user = (result[2], result[3])
                    logged_in = True
                    print("Logged in!")
                else:
                    print("Login failed!")
            if selection == "2":
                register_page()
            if selection == "3":
                break


if __name__ == '__main__':
    main()
