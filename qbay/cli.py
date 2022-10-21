from qbay.models import update_listing


def update_listing_page():
    '# loop until they want to exit'
    while True:
        listing = input('Please enter the listing id of the listing you want '
                        'to update: ')
        selection = input('Press 1 to update the title, 2 to update the '
                          'description, 3 to update the price, 4 to update '
                          'the address, and 5 to exit.')
        if selection == 1:
            title = input('Enter the new title for your listing: ')
        elif selection == 2:
            description = input('Enter the new description for your '
                                'listing: ')
        elif selection == 3:
            price = input('Enter the new price per night (in whole dollars: ')
            try:
                price = int(price)
                # 1 should be replaced with the listing id
                flag, msg = update_listing(listing, title, description, price, 
                                           address)
                if flag is False:
                    print('Listing not updated')
                    print(msg)
                else:
                    print('Listing updated')
                    print('Title: ', title)
                    print('Description: ', address)
                    print('Address: ', description)
                    print('Price: $', price)
            except ValueError:
                print('Price must be an integer')
        elif selection == 4:
            address = input('Enter the new address for your listing: ')
        elif selection == 5:
            # user homepage fuction should replace break
            break
        
