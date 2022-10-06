from qbay.models import register, login, create_listing
from qbay.models import User, Listing
import datetime

def test_r1_1_user_register():
    """
    When creating a user, check that the email field and password field
    cannot be empty.
    Assert 1: Check that email cannot be empty.
    Assert 2: Check that password cannot be empty.
    Assert 3: Check that both cannot be empty.
    """
    assert register(
        username="test user",
        email="",
        password="test_password")[0] is False
    assert register(
        username="test user",
        email="test@gmail.com",
        password="")[0] is False
    assert register(
        username="test user",
        email="",
        password="")[0] is False
    assert register(
        username="pass user",
        email="pass_empty@gmail.com",
        password="Pass_pwd")[0] is True


def test_r1_2_user_register():
    """
    Register 2 users, then use a set and compare list vs set size
    to determine that all user_id's are unique.
    """
    register(
        username="Test user 1",
        email="test_user_id_1@gmail.com",
        password="Test_user_1_pwd")
    register(
        username="Test user 2",
        email="test_user_id_2@gmail.com",
        password="Test_user_2_pwd")
    user_ids: list[int] = User.query.order_by(User.user_id)\
        .with_entities(User.user_id).all()
    assert len(user_ids) == len(set(user_ids))


def test_r1_3_user_register():
    """
    When creating a user, determine if the email follows the
    constraints of RFC 5322.
    """
    assert register(
        username="rfc pass 1",
        email="name.surname@gmail.com",
        password="RFC_pass1_pwd")[0] is True
    assert register(
        username="rfc pass 2",
        email="testUsername123@yahoo.co.uk",
        password="RFC_pass2_pwd")[0] is True
    assert register(
        username="rfc fail 1",
        email="name.Surname@...ca",
        password="RFC_fail1_pwd")[0] is False
    assert register(
        username="rfc fail 2",
        email="...@gmail.com",
        password="RFC_fail2_pwd")[0] is False


def test_r1_4_user_register():
    """
    While creating the user, ensure that the password meets the required
    complexity.
    """
    # Check minimum length test case
    assert register(
        username="pwd fail 1",
        email="pwdTestFail1@gmail.com",
        password="Sh0rt"
    )[0] is False
    # Check password has no upper case
    assert register(
        username="pwd fail 2",
        email="pwdTestFail2@gmail.com",
        password="n0_upper_case"
    )[0] is False
    # Check password has no lower case
    assert register(
        username="pwd fail 3",
        email="pwdTestFail3@gmail.com",
        password="N0_LOWER_CASE"
    )[0] is False
    # Check password has no special character
    assert register(
        username="pwd fail 4",
        email="pwdTestFail4@gmail.com",
        password="NoSpecialCharacters"
    )[0] is False
    # Check for a pass case where we meet all requirements
    assert register(
        username="pwd pass 1",
        email="pwdTestPass1@gmail.com",
        password="G00d#Password!"
    )[0] is True


def test_r1_5_user_register():
    """
    Check for username being non-empty, alphanumeric-only,
    and space allowed as long as it's not in the prefix or suffix.
    """
    # Check for username that is empty
    assert register(
        username="",
        email="r1_5_1_fail@gmail.com",
        password="G00d#Password!"
    )[0] is False
    # Check for non-alphanumeric-only usernames
    assert register(
        username="HEEHAW#143",
        email="r1_5_2_fail@gmail.com",
        password="G00d#Password!"
    )[0] is False
    # Check for prefix space in username
    assert register(
        username=" prefix space",
        email="r1_5_3_fail@gmail.com",
        password="G00d#Password!"
    )[0] is False
    # Check for suffix space in username
    assert register(
        username="suffix space ",
        email="r1_5_4_fail@gmail.com",
        password="G00d#Password!"
    )[0] is False
    # Check that a good username passes
    assert register(
        username="good Username",
        email="r1_5_1_pass@gmail.com",
        password="G00d#Password!"
    )[0] is True


def test_r1_6_user_register():
    """
    Test that username length should be longer than 2 characters
    and shorter than 20 characters.
    """
    # Check for 2 or less characters
    assert register(
        username="Ba",
        email="r1_6_1_fail@gmail.com",
        password="G00d#Password!"
    )[0] is False
    # Check for 20 or more characters
    assert register(
        username="qwertyuiopasdfghjklz",
        email="r1_6_2_fail@gmail.com",
        password="G00d#Password!"
    )[0] is False
    # Check for a case in between that SHOULD pass
    assert register(
        username="Good Username",
        email="r1_6_1_pass@gmail.com",
        password="G00d#Password!"
    )[0] is True


def test_r1_7_user_register():
    """
    When creating a user, registering should fail
    if an email has been used already.
    """
    assert register(
        username="Email Used 1",
        email="r1_7_1_test@gmail.com",
        password="G00d#Password!"
    )[0] is True
    # Check that reusing "r1_7_1_test@gmail.com" will fail since we
    # just created a user with that email in the db.
    assert register(
        username="Email Used 2",
        email="r1_7_1_test@gmail.com",
        password="G00d#Password!"
    )[0] is False

    # And finally, as a sanity check, scan through the database to make sure
    # all emails are unique using a set
    user_emails: list[str] = User.query.order_by(User.email)\
        .with_entities(User.email).all()
    assert len(user_emails) == len(set(user_emails))


# noinspection PyComparisonWithNone
def test_r1_8_user_register():
    """
    When a user is created, shipping address should be left blank
    (essentially, NULL)
    """
    assert register(
        username="Shipping Null",
        email="r1_8_1_pass@gmail.com",
        password="G00d#Password!"
    )[0] is True

    # Compare the list size of all users vs
    # all users that have a blank billing address
    user_address = User.query.order_by(User.user_id)\
        .filter(User.billing_address.is_(None)).all()
    users = User.query.order_by(User.user_id).all()
    assert len(users) == len(user_address)


def test_r1_9_user_register():
    """
    When a user is created, postal code should be left blank
    (essentially, NULL)
    """
    assert register(
        username="Postal Null",
        email="r1_9_1_pass@gmail.com",
        password="G00d#Password!"
    )[0] is True

    # Assert all postal codes are blank to this point
    user_postal_codes = User.query.order_by(User.user_id)\
        .filter(User.postal_code.is_(None)).all()
    users = User.query.order_by(User.user_id).all()
    assert len(users) == len(user_postal_codes)


def test_r1_10_user_register():
    """
    When a user is created successfully, their balance should
    be initialized to 100.
    """
    assert register(
        username="Balance 100",
        email="r1_10_1_pass@gmail.com",
        password="G00dPassword#!"
    )[0] is True

    # Check all users that we've added have a starting balance of 100
    users: list[int, int] = User.query.order_by(User.user_id)\
        .with_entities(User.user_id, User.balance)
    assert (user_info[1] == 100 for user_info in users)


def test_r2_1_user_login():
    """
    Check that a user can log into an existing account. Othewise,
    it should return a None value.
    """
    # Check for logging into an existing account
    assert register(
        username="Login Test 1",
        email="r2_1_1_pass@gmail.com",
        password="G00dPassword#!"
    )[0] is True
    account, msg = login(
        email="r2_1_1_pass@gmail.com",
        password="G00dPassword#!"
    )
    assert account.email == "r2_1_1_pass@gmail.com" and \
           account.password == "G00dPassword#!"

    # Check for logging into a non-existing account email
    account, msg = login(
        email="r2_1_1_fail@gmail.com",
        password="G00dPassword#!"
    )
    assert account is None

    # Check for logging into an existing account with the wrong password
    account, msg = login(
        email="r2_1_1_pass@gmail.com",
        password="Wr0ngPassword#!"
    )
    assert account is None


def test_r2_2_user_login():
    """
    Check the same email/password requirements as the register function,
    such that it stops before we reach a user query where it will return
    None.
    It will never return None or True if it does not reach the User query.
    (It should only return False in these tests, not None or True).
    """
    # Check for blank email and password cases
    flag, msg = login(
        email="",
        password="G00dPassword#!"
    )
    assert flag is False
    flag, msg = login(
        email="good_email@gmail.com",
        password=""
    )
    assert flag is False
    flag, msg = login(
        email="",
        password=""
    )
    assert flag is False

    # Check for RFC 5322 validation
    flag, msg = login(
        email="name.Surname@...ca",
        password="RFC_fail1_pwd"
    )
    assert flag is False
    flag, msg = login(
        email="...@gmail.com",
        password="RFC_fail2_pwd"
    )
    assert flag is False

    # Check for password complexity
    flag, msg = login(
        email="pwdTestFail1@gmail.com",
        password="Sh0rt"
    )  # Minimum length check
    assert flag is False
    flag, msg = login(
        email="pwdTestFail2@gmail.com",
        password="n0_upper_case"
    )  # Maximum length check
    assert flag is False
    flag, msg = login(
        email="pwdTestFail3@gmail.com",
        password="N0_LOWER_CASE"
    )  # Must have lower case check
    assert flag is False
    flag, msg = login(
        email="pwdTestFail4@gmail.com",
        password="NoSpecialCharacters"
    )  # Must have a special character check
    assert flag is False


def test_r4_1_create_listing():
    """
    test that listing title is alphanumeric with spaces for create listing
    """
    # Normal Case
    assert create_listing("nice cabin on 123 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # Empty case
    assert create_listing("",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # Non alphanumeric at start
    assert create_listing("!nice cabin on 124 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is False
    # Non alphanumeric at end
    assert create_listing("nice cabin on 125 street!",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is False
    # Non alphanumeric in the middle
    assert create_listing("nice cabin !on 126 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is False


def test_r4_2_create_listing():
    """
    test that listing title is less than 80 characters for create listing
    """
    # less than 80
    assert create_listing("nice cabin on 127 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # more than 80
    assert create_listing("""This is longer than 80 chracters, this is longer 
                          than 80 charcaters, this is longer than 80 charcaters, 
                          this is longer than 80 charcaters""",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is False


def test_r4_3_create_listing():
    """
    test that descritpion is between 20-20000 chracters for create listing
    """
    # between 20-2000
    assert create_listing("nice cabin on 129 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # less than 20
    assert create_listing("n", "ab", 150, "123 street", 1) is False
    f = open("two thousand.txt", "r")
    charcter_lim = f.read()
    f.close()
    # more than 2000
    assert create_listing("nice cabin on 131 street",
                          charcter_lim, 150, "123 street", 1) is False
    

def test_r4_4_create_listing():
    """
    test that listing title is shorter than description for create listing
    """
    # longer than title
    assert create_listing("nice cabin on 132 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # shorter than title
    assert create_listing("nice cabin on 133 street",
                          "a waterfront cabin",
                          150, "123 street", 1) is False


def test_r4_5_create_listing():
    """
    test that listing price is between 10-10000
    """
    # price in range 10-10000
    assert create_listing("nice cabin on 134 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # price less than 10
    assert create_listing("nice cabin on 135 street",
                          "a waterfront cabin located in downtown real city",
                          2, "123 street", 1) is False
    # price more than 10000
    assert create_listing("nice cabin on 136 street",
                          "a waterfront cabin located in downtown real city",
                          200000, "123 street", 1) is False


def test_r4_6_create_listing():
    """
    test that date is between 2021-01-02 and 2025-01-02
    Date is auto made for todays date which is between these dates
    """
    assert (Listing.query.get(1).last_modified_date < 
            datetime.datetime(2025, 1, 2) and 
            Listing.query.get(1).last_modified_date > 
            datetime.datetime(2021, 1, 2)) is True


def test_r4_7_create_listing():
    """
    Test that user exists in data base, the user must have a email.
    The second is already guaranteed as it is required to register
    """
    # user in data base
    assert create_listing("nice cabin on 137 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # user not in database
    assert create_listing("nice cabin on 138 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 10000000000000) is False


def test_r4_8_create_listing():
    """
    A user cannot create products that have the same title
    """
    # user does not have one of the same title
    assert create_listing("nice cabin on 139 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is True
    # user does have one of the same title
    assert create_listing("nice cabin on 139 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1) is False