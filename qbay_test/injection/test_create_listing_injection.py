from qbay.models import create_listing
from pathlib import Path


def test_create_listing_injection_title():
    """
        This function uses the injection.txt file to
        inject different lines into the "title" argument
        of the create_listing function to ensure that there
        is no weakpoint in the code that could be exploited
        
    """
    current_folder = Path(__file__).parent
    f = open(current_folder.joinpath('injection.txt'))
    lines = f.readlines()
    f.close
    for line in lines:
        create_listing(title=line,
                       description="This is a sample description",
                       price=50,
                       address="123 queen st",
                       user_id=1)


# The following functions repeat the above with their respective argument
def test_create_listing_injection_description():
    current_folder = Path(__file__).parent
    f = open(current_folder.joinpath('injection.txt'))
    lines = f.readlines()
    f.close
    i = 0
    for line in lines:
        title = 'Test Injection title' + str(i)
        create_listing(title=title,
                       description=line,
                       price=50,
                       address="123 queen st",
                       user_id=1)
        i += 1


def test_create_listing_injection_price():
    current_folder = Path(__file__).parent
    f = open(current_folder.joinpath('injection.txt'), 'r')
    i = 0
    for line in f.readlines():
        title = 'Test Injection title' + str(i)
        create_listing(title=title,
                       description="This is a sample description",
                       price=line,
                       address="123 Avenue ave.",
                       user_id=1)
        i += 1
    f.close()
    

def test_create_listing_injection_address():
    current_folder = Path(__file__).parent
    f = open(current_folder.joinpath('injection.txt'), 'r')
    i = 0
    for line in f.readlines():
        title = 'Test Injection title' + str(i)
        create_listing(title=title,
                       description="This is a sample description",
                       price=50,
                       address=line,
                       user_id=1)
        i += 1
    f.close()


def test_create_listing_injection_user():
    current_folder = Path(__file__).parent
    f = open(current_folder.joinpath('injection.txt'), 'r')
    i = 0
    for line in f.readlines():
        title = 'Test Injection title' + str(i)
        create_listing(title=title,
                       description="This is a sample description",
                       price=50,
                       address="123 Avenue ave.",
                       user_id=line)
        i += 1
    f.close()
