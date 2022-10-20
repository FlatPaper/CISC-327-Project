from qbay.models import create_listing


def create_listing_page():
    # loop till they choose to exit
    while True:
        selection = input('Press 1 to make a listing or 2 to exit the page')
        if selection == 1:
            title = input('Enter the title of your listing: ')
            address = input('Enter the address of your property: ')
            description = input('Enter the description of your property: ')
            price = input('Enter the price per night (whole dollars): ')
            try:
                price = int(price)
                # replace the 1 with the currently logged in user
                flag, msg = create_listing(title, description, price, address,
                                           1)
                if flag is False:
                    print('Listing not created')
                    print(msg)
                else:
                    print('Listing created')
                    print('Title: ', title)
                    print('Address: ', address)
                    print('Description: ', description)
                    print('Price: $', price)
            except ValueError:
                print('Price needs to be an integer')

        elif selection == 2:
            # replace the break with user home page function
            break 

    