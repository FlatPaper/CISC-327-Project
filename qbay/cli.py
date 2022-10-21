from qbay.models import register, login, update_user_profile, create_listing


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
    username = input('Please input updated username: ')
    email = input('Please input updated email: ')
    address = input('Please input updated address: ')
    postal_code = input('Please input updated postal code: ')

    update_username = len(username) > 0
    update_email = len(email) > 0
    update_address = len(address) > 0
    update_postal_code = len(postal_code) > 0

    if not update_username:
        username = None
    if not update_email:
        email = None
    if not update_address:
        address = None
    if not update_postal_code:
        postal_code = None

    return update_user_profile(user_id, username, email, address, postal_code)


def create_listing_page(current_user):
    while True:
        selection = input('Press 1 to make a listing or 2 to exit the page: ')
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
                    print(msg)
                    print("Listing not created.")
                else:
                    print("Listing created")
                    print("Title: {}".format(title))
                    print("Address: {}".format(address))
                    print("Description: {}".format(description))
                    print("Price: ${}".format(price))
            except ValueError:
                print('Price needs to be an integer.')
        if selection == "2":
            break
