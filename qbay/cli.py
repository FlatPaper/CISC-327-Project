from qbay.models import register


def register_page():
    email = input('Please input email: ')
    username = input('Please input a username: ')
    password = input('Please input password: ')
    password_twice = input('Please input the password again: ')

    if password != password_twice:
        print("Password entered is not the same.")

    result = register(email=email, username=username, password=password)
    if result[0]:
        print(result[1])
        print('Registration succeeded.')
    else:
        print(result[1])
        print('Registration failed.')
