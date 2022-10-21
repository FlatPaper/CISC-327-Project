from qbay.models import create_listing, register, login


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


def create_listing_page(current_user):
    while True:
        selection = input('Press 1 to make a listing or 2 to exit the page')
        if selection == "1":
            title = input('Enter the title of your listing: ')
            address = input('Enter the address of your property: ')
            description = input('Enter the description of your property: ')
            price = input('Enter the price per night (whole dollars): ')
            try:
                price = int(price)
                flag, msg = create_listing(title, description, price, address,
                                           current_user)
                if flag is False:
                    print("Listing not created")
                    print(msg)
                else:
                    print("Listing created")
                    print("Title: {}".format(title))
                    print("Address: {}".format(address))
                    print("Description: {}".format(description))
                    print("Price: ${}".format(price))
            except ValueError:
                print('Price needs to be an integer')

        elif selection == 2:
            break
