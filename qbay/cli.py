from qbay.models import register, login, update_user_profile


def register_page():
    email = input('Please input email: ')
    username = input('Please input a username: ')
    password = input('Please input password: ')
    password_twice = input('Please input the password again: ')

    if password != password_twice:
        print(
            "Passwords entered are not the same.\n"
            "Registration failed."
        )
        return False, "Password entered is not the same."

    result = register(email=email, username=username, password=password)
    if result[0]:
        print(result[1])
        print('Registration succeeded.')
    else:
        print(result[1])
        print('Registration failed.')


def login_page():
    email = input('Please input email: ')
    password = input('Please input password: ')

    result = login(email=email, password=password)
    return result[0], result[1], email, password


def update_user_page(user_id):
    username = input('Please input updated username:')
    email = input('Please input updated email:')
    address = input('Please input updated address:')
    postal_code = input('Please input updated postal code:')
    return update_user_profile(user_id, username, email, address, postal_code)
