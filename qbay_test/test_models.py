from qbay.models import register, login, update_user_profile
from qbay.models import create_listing, update_listing, book_listing
from qbay.models import User, Listing

from datetime import datetime, date


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
    user_ids: list[int] = User.query.order_by(User.user_id) \
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
    user_emails: list[str] = User.query.order_by(User.email) \
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
    user_address = User.query.order_by(User.user_id) \
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
    user_postal_codes = User.query.order_by(User.user_id) \
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
    users: list[int, int] = User.query.order_by(User.user_id) \
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


def test_r3_1_update_user_profile():
    """
    User should only be able to update username, email, billing address,
    and postal code.
    """
    assert register(
        username="test user r3 1",
        email="r3_1_test@gmail.com",
        password="G00dPassword#!"
    )[0] is True

    user = User.query.filter_by(email="r3_1_test@gmail.com").all()[0]

    # Check update function works correctly
    assert update_user_profile(user.user_id,
                               username="updated user",
                               email="updated@gmail.com",
                               billing_address="321 updated dr",
                               postal_code="L9R0T9")[0] is True

    user = User.query.filter_by(email="updated@gmail.com").all()[0]
    assert (user.username == "updated user" and
            user.email == "updated@gmail.com" and
            user.billing_address == "321 updated dr" and
            user.postal_code == "L9R0T9") is True


def test_r3_2_update_user_profile():
    """
    Postal code should be non-empty, alphanumeric, and no special characters.
    """
    user = User.query.filter_by(email="updated@gmail.com").all()[0]

    assert update_user_profile(
        user.user_id,
        postal_code="123456")[0] is False

    assert update_user_profile(
        user.user_id,
        postal_code="ABCDEF")[0] is False

    assert update_user_profile(
        user.user_id,
        postal_code="@#$%^&")[0] is False

    # Check valid postal code
    assert update_user_profile(
        user.user_id,
        postal_code="K7T9Y2")[0] is True


def test_r3_3_update_user_profile():
    """
    Check if postal code is valid Canadian postal code in format A1A 1A1,
    where A's are a letter and 1's are a number.
    """

    user = User.query.filter_by(email="updated@gmail.com").all()[0]

    # Check wrongly formatted postal code
    assert update_user_profile(
        user.user_id,
        postal_code="7T0P8W")[0] is False

    # Check valid Canadian postal code
    assert update_user_profile(
        user.user_id,
        postal_code="K7W0T9")[0] is True


def test_r3_4_update_user_profile():
    """
    Updating username should follow the same constraints as when registering.
    Checks for username being non-empty, alphanumeric-only, and space allowed
    as long as it's not in the prefix or suffix.
    """

    user = User.query.filter_by(email="updated@gmail.com").all()[0]

    # Check for empty username
    assert update_user_profile(user.user_id,
                               username=""
                               )[0] is False
    # Check for non-alphanumeric only usernames
    assert update_user_profile(user.user_id,
                               username="HeLlo$123"
                               )[0] is False
    # Check for prefix space in username
    assert update_user_profile(user.user_id,
                               username=" HeLlo123"
                               )[0] is False
    # Check for suffix space in username
    assert update_user_profile(user.user_id,
                               username="HeLlo123 "
                               )[0] is False
    # Check for a valid username
    assert update_user_profile(user.user_id,
                               username="valid username"
                               )[0] is True


def test_r4_1_create_listing():
    """
    test that listing title is alphanumeric with spaces for create listing
    """

    # Normal Case
    assert create_listing("nice cabin on 123 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is True
    # prefix case
    assert create_listing(" test",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is False
    # suffix case
    assert create_listing("test ",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is False
    # Non-alphanumeric
    assert create_listing("!nice cabin on 124 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is False


def test_r4_2_create_listing():
    """
    test that listing title is less than 80 characters for create listing
    """
    # less than 80
    assert create_listing("nice cabin on 127 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is True
    # more than 80
    test_str = "a" * 90
    assert create_listing(test_str,
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is False


def test_r4_3_create_listing():
    """
    test that description is between 20-20000 characters for create listing
    """
    # between 20-2000
    assert create_listing("nice cabin on 129 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is True
    # less than 20
    assert create_listing("n", "ab", 150, "123 street", 1)[0] is False

    long_desc = "a" * 3000
    # more than 2000
    assert create_listing("nice cabin on 131 street",
                          long_desc, 150, "123 street", 1)[0] is False


def test_r4_4_create_listing():
    """
    test that listing title is shorter than description for create listing
    """
    # longer than title
    assert create_listing("nice cabin on 132 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is True
    # shorter than title
    assert create_listing("nice cabin on 133 street",
                          "a waterfront cabin",
                          150, "123 street", 1)[0] is False


def test_r4_5_create_listing():
    """
    test that listing price is between 10-10000
    """
    # price in range 10-10000
    assert create_listing("nice cabin on 134 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is True
    # price less than 10
    assert create_listing("nice cabin on 135 street",
                          "a waterfront cabin located in downtown real city",
                          2, "123 street", 1)[0] is False
    # price more than 10000
    assert create_listing("nice cabin on 136 street",
                          "a waterfront cabin located in downtown real city",
                          200000, "123 street", 1)[0] is False


def test_r4_6_create_listing():
    """
    test that date is between 2021-01-02 and 2025-01-02
    Date is auto made for today's date which is between these dates
    """
    assert (datetime(2025, 1, 2) >
            Listing.query.get(1).last_modified_date >
            datetime(2021, 1, 2)) is True


def test_r4_7_create_listing():
    """
    Test that user exists in database, the user must have a email.
    The second is already guaranteed as it is required to register
    """
    # user in data base
    assert create_listing("nice cabin on 137 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is True
    # user not in database
    assert create_listing("nice cabin on 138 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 10000000000000)[0] is False


def test_r4_8_create_listing():
    """
    A user cannot create products that have the same title
    """
    # user does not have one of the same title
    assert create_listing("nice cabin on 139 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is True
    # user does have one of the same title
    assert create_listing("nice cabin on 139 street",
                          "a waterfront cabin located in downtown real city",
                          150, "123 street", 1)[0] is False


def test_r5_1_updating_all_attributes():
    """
        Update each listing attribute once to show that they can be updated
    """

    register(
        username="Test user 1",
        email="test_user_id_1@gmail.com",
        password="Test_user_1_pwd")

    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    create_listing(
        title="Test Title R5 1",
        description="A description that is long",
        price=100,
        address="123 Street St.",
        user_id=user_test.user_id)

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 1").all()[0]

    # Updates each listing attribute
    assert update_listing(listing_id=listing_test.listing_id,
                          title="Test Title R5 1 1",
                          description="Another description that is longer",
                          price=120,
                          address="124 Street")[0] is True
    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 1 1").all()[0]
    assert listing_test.title == "Test Title R5 1 1"
    assert listing_test.description == "Another description that is longer"
    assert listing_test.price == 120
    assert listing_test.address == "124 Street"


def test_r5_2_update_listing_price():
    """
        Check that price can only be increased.
    """

    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    assert create_listing(
        title="Test Title R5 2",
        description="A description that is long",
        price=10,
        address="123 Street St.",
        user_id=user_test.user_id)[0] is True

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 2").all()[0]

    # Price is less than 10
    assert update_listing(
        listing_id=listing_test.listing_id,
        price=5,
        address="123 Street St.")[0] is False

    # Price between 10-1000
    assert update_listing(
        listing_id=listing_test.listing_id,
        price=200,
        address="123 Street St.")[0] is True

    # Price is more than 1000
    assert update_listing(
        listing_id=listing_test.listing_id,
        price=4000,
        address="123 Street St.")[0] is False


def test_r5_3_update_last_date_modified():
    """
        Check that the last_date_modified is less than the current date
        to ensure that it has successfully updated.
    """

    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    assert create_listing(
        title="Test Title R5 3",
        description="A description that is long",
        price=10,
        address="123 Street St.",
        user_id=user_test.user_id)[0] is True

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 3").all()[0]

    update_listing(
        listing_id=listing_test.listing_id,
        price=400,
        address="123 Street St.")

    listing_test_after: Listing = Listing.query.filter_by(
        title="Test Title R5 3").all()[0]

    assert (datetime.today().year == listing_test_after.last_modified_date.year
            and datetime.today().month ==
            listing_test_after.last_modified_date.month
            and datetime.today().day ==
            listing_test_after.last_modified_date.day
            and datetime.today().hour ==
            listing_test_after.last_modified_date.hour
            and datetime.today().minute ==
            listing_test_after.last_modified_date.minute)


def test_r5_4_1_update_listing():
    """
    test that listing title is alphanumeric with spaces for update listing.
    """
    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    assert create_listing(
        title="Test Title R5 4",
        description="A description that is long",
        price=10,
        address="123 Street St.",
        user_id=user_test.user_id)[0] is True

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4").all()[0]

    # Normal Case
    assert update_listing(
        listing_id=listing_test.listing_id,
        title="nice cabin on 123 street test")[0] is True

    # prefix case
    assert update_listing(
        listing_id=listing_test.listing_id,
        title=" test")[0] is False

    # suffix case
    assert update_listing(
        listing_id=listing_test.listing_id,
        title="test ")[0] is False

    # Non-alphanumeric
    assert update_listing(
        listing_id=listing_test.listing_id,
        title="sdf#$ heh!")[0] is False


def test_r5_4_2_update_listing():
    """
    test that listing title is less than 80 characters for update listing.
    """
    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    assert create_listing(
        title="Test Title R5 4",
        description="A description that is long",
        price=10,
        address="123 Street St.",
        user_id=user_test.user_id)[0] is True

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4").all()[0]

    # less than 80
    assert update_listing(
        listing_id=listing_test.listing_id,
        title="nice cabin on 127 street 2")[0] is True

    # more than 80
    test_str = "a" * 90
    assert update_listing(
        listing_id=listing_test.listing_id,
        title=test_str)[0] is False


def test_r5_4_3_update_listing():
    """
    test that description is between 20-20000 characters for update listing.
    """
    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    assert create_listing(
        title="Test Title R5 4 3",
        description="A description that is long",
        price=10,
        address="123 Street St.",
        user_id=user_test.user_id)[0] is True

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4 3").all()[0]

    # between 20-2000
    test_str = "a" * 25
    assert update_listing(
        listing_id=listing_test.listing_id,
        description=test_str
    )[0] is True

    # less than 20
    assert update_listing(
        listing_id=listing_test.listing_id,
        description="heh fail"
    )[0] is False

    # more than 2000
    long_desc = "a" * 3000
    assert update_listing(
        listing_id=listing_test.listing_id,
        description=long_desc
    )[0] is False


def test_r5_4_4_update_listing():
    """
    test that listing title is shorter than description for update listing.
    """
    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    assert create_listing(
        title="Test Title R5 4 4",
        description="A description that is long",
        price=10,
        address="123 Street St.",
        user_id=user_test.user_id)[0] is True

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4 4").all()[0]

    # longer than title
    test_desc = "b" * 40
    assert update_listing(
        listing_id=listing_test.listing_id,
        description=test_desc
    )[0] is True

    # shorter than title
    test_desc = "b" * 5
    assert update_listing(
        listing_id=listing_test.listing_id,
        description=test_desc
    )[0] is False


def test_r5_4_5_update_listing():
    """
    test that listing price is between 10-10000
    """
    user_test: User = User.query.filter_by(
        email="test_user_id_1@gmail.com").all()[0]

    assert create_listing(
        title="Test Title R5 4 5",
        description="A description that is long",
        price=10,
        address="123 Street St.",
        user_id=user_test.user_id)[0] is True

    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4 5").all()[0]

    # price in range 10-10000
    assert update_listing(
        listing_id=listing_test.listing_id,
        price=50
    )[0] is True
    # price less than 10
    assert update_listing(
        listing_id=listing_test.listing_id,
        price=2
    )[0] is False
    # price more than 10000
    assert update_listing(
        listing_id=listing_test.listing_id,
        price=99999
    )[0] is False


def test_r5_4_6_update_listing():
    """
    test that date is between 2021-01-02 and 2025-01-02
    Date is auto made for today's date which is between these dates.
    """
    # use previous unit tests listing model to test this
    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4 5").all()[0]

    assert (datetime(2025, 1, 2) >
            listing_test.last_modified_date >
            datetime(2021, 1, 2)) is True


def test_r5_4_7_update_listing():
    """
    Test that after updating a listing, it should have an owner email,
    and that the owner email exists.
    """
    # Use the last unit test Listing model to find this out
    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4 5").all()[0]

    # user in data base
    assert update_listing(
        listing_id=listing_test.listing_id,
        address="New Test Address"
    )[0] is True
    assert listing_test.user_id is not None

    assert User.query.get(listing_test.user_id) is not None


def test_r5_4_8_update_listing():
    """
    A user cannot create products that have the same title.
    """
    # use previous unit tests listing model to test this
    listing_test: Listing = Listing.query.filter_by(
        title="Test Title R5 4 5").all()[0]

    # user does not have one of the same title
    assert update_listing(
        listing_id=listing_test.listing_id,
        title="Test Title R5 4 8"
    )[0] is True

    # user does have one of the same title
    assert update_listing(
        listing_id=listing_test.listing_id,
        title="Test Title R5 4 3"
    )[0] is False


def test_r6_1_book_listing():
    """
    Check a user can book a listing.
    """
    # Create two accounts to validate booking system
    assert register(
        username="valid user 1",
        email="valid1@gmail.com",
        password="GoodPass!"
    )[0] is True

    assert register(
        username="valid user 2",
        email="valid2@gmail.com",
        password="GoodPass!"
    )[0] is True

    user1 = User.query.filter_by(email="valid1@gmail.com").all()[0]
    user2 = User.query.filter_by(email="valid2@gmail.com").all()[0]

    # Create listing for user 2
    assert create_listing(
        "User 2 Test House",
        "A nice house in the city",
        50, "123 University Av", user2.user_id)[0] is True

    listing = Listing.query.filter_by(title="User 2 Test House").all()[0]

    # User 1 books user 2's listing
    assert book_listing(
        listing.listing_id, user1.user_id, date(2022, 12, 30)
    )[0] is True


def test_r6_2_book_listing():
    """
    User cannot book their own listing.
    """
    assert register(
        username="single user",
        email="email@gmail.com",
        password="GoodPass!"
    )[0] is True

    user = User.query.filter_by(email="email@gmail.com").all()[0]

    assert create_listing(
        "User 1 Test House",
        "This is a very cool house!",
        50, "123 University Av", user.user_id)[0] is True
    
    listing = Listing.query.filter_by(title="User 1 Test House").all()[0]

    assert book_listing(
        listing.listing_id, user.user_id, date(2022, 12, 30)
    )[0] is False


def test_r6_3_book_listing():
    """
    User cannot book listing more than their balance.
    """
    # Create two accounts to check whether booking can be made if user
    # has insufficient funds
    assert register(
        username="user 1",
        email="userone@gmail.com",
        password="GoodPass!"
    )[0] is True

    assert register(
        username="user 2",
        email="usertwo@gmail.com",
        password="GoodPass!"
    )[0] is True

    user1 = User.query.filter_by(email="userone@gmail.com").all()[0]
    user2 = User.query.filter_by(email="usertwo@gmail.com").all()[0]

    # Create listing for user 2, cost $101
    assert create_listing(
        "Test House",
        "A very cool and interesting house description",
        101, "123 University Av", user2.user_id)[0] is True

    listing = Listing.query.filter_by(title="Test House").all()[0]

    # User 1 tries to book user 2's listing
    assert book_listing(
        listing.listing_id, user1.user_id, date(2022, 12, 30)
    )[0] is False


def test_r6_4_book_listing():
    """
    User cannot book a listing that is already booked with
    the overlapped dates.
    """
    # Create 3 users to test that an already booked listing
    # cannot be rebooked
    assert register(
        username="test user 1",
        email="user1@gmail.com",
        password="GoodPass!"
    )[0] is True

    assert register(
        username="test user 2",
        email="user2@gmail.com",
        password="GoodPass!"
    )[0] is True

    assert register(
        username="test user 3",
        email="user3@gmail.com",
        password="GoodPass!"
    )[0] is True

    user1 = User.query.filter_by(email="user1@gmail.com").all()[0]
    user2 = User.query.filter_by(email="user2@gmail.com").all()[0]
    user3 = User.query.filter_by(email="user3@gmail.com").all()[0]

    # Create listing for user 2
    assert create_listing(
        "User Two Test House",
        "A very cool and interesting house description",
        50, "123 University Av", user2.user_id)[0] is True

    listing = Listing.query.filter_by(title="User Two Test House").all()[0]

    # User 1 books user 2's listing
    assert book_listing(
        listing.listing_id, user1.user_id, date(2023, 12, 30)
    )[0] is True
    # User 3 also tries to book user 2's listing on the same day as user 1
    assert book_listing(
        listing.listing_id, user3.user_id, date(2023, 12, 30)
    )[0] is False
    # User 3 books user 2's listing a day after user 1
    assert book_listing(
        listing.listing_id, user3.user_id, date(2023, 12, 31)
    )[0] is True
