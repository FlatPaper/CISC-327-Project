from qbay.models import register
from qbay.models import User


def test_r1_1_user_register():
    """
    When creating a user, check that the email field and password field
    cannot be empty.
    Assert 1: Check that email cannot be empty.
    Assert 2: Check that password cannot be empty.
    Assert 3: Check that both cannot be empty.
    """
    assert register(
        username="test_user",
        email="",
        password="test_password")[0] is False
    assert register(
        username="test_user",
        email="test@gmail.com",
        password="")[0] is False
    assert register(
        username="test_user",
        email="",
        password="")[0] is False
    assert register(
        username="pass user",
        email="pass@gmail.com",
        password="Pass_pwd")[0] is True


def test_r1_2_user_register():
    """
    Let's create 2 unique users, then determine whether or not their ID
    is unique.
    """
    register(
        username="Test user 1",
        email="test_user_1@gmail.com",
        password="Test_user_1_pwd")
    register(
        username="Test user 2",
        email="test_user_2@gmail.com",
        password="Test_user_2_pwd")
    users: list[User] = User.query.order_by(User.user_id).all()
    assert users[0].user_id != users[1].user_id


def test_r1_3_user_register():
    """
    When creating a user, determine whether or not the email follows the
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
