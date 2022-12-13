from qbay.models import book_listing
from pathlib import Path
from datetime import date


def test_book_listing_injection_listing_id():
    """
        This function uses the injection.txt file to
        inject different lines into the "listing_id" argument
        of the book_listing function to ensure that there
        is no weakpoint in the code that could be exploited

    """
    current_folder = Path(__file__).parent
    f = open(current_folder.joinpath('injection.txt'), 'r')
    lines = f.readlines()
    f.close
    for line in lines:
        book_listing(listing_id=line,
                     user_id=2,
                     booked_date=date(2023, 4, 4))


# The following functions repeat the above with their respective argument
def test_book_listing_injection_user_id():
    current_folder = Path(__file__).parent
    f = open(current_folder.joinpath('injection.txt'), 'r')
    lines = f.readlines()
    f.close
    for line in lines:
        book_listing(listing_id=1,
                     user_id=line,
                     booked_date=date(2023, 4, 4))
