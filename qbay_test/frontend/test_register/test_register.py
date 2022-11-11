from pathlib import Path
import subprocess

# get expected input/output folder
current_folder = Path(__file__).parent


def test_register1():
    """
    Let's test first by **input partition method** based on:
    Empty email | non RFC email
    empty username | username length < 2 | username length > 20 |
    username contains special characters | username has space in prefix
    empty password | password length < 6 | password has no uppercase |
    password has no lowercase | password has no special characters |
    good account
    (test_register3.in passes, rest should fail)
    """
    for i in range(1, 14):
        str_in = "input_partition/test_register" + str(i) + ".in"
        str_out = "input_partition/test_register" + str(i) + ".out"
        expected_in = open(current_folder.joinpath(str_in))
        expected_out = open(current_folder.joinpath(str_out)).read()

        # print("\n\nEXPECTED OUTPUT")
        # print(expected_out)
        # print("\n\n")

        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()
        #
        # print('---------------------------')
        # print('outputs',output)
        # print('---------------------------')

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()


def test_register2():
    """
    Output partition method
    Should either succeed or not - user should be created or failed to create.
    (test_register15.in should pass, 14 should fail)
    """
    for i in range(14, 16):
        str_in = "input_partition/test_register" + str(i) + ".in"
        str_out = "input_partition/test_register" + str(i) + ".out"
        expected_in = open(current_folder.joinpath(str_in))
        expected_out = open(current_folder.joinpath(str_out)).read()

        # print("\n\nEXPECTED OUTPUT")
        # print(expected_out)
        # print("\n\n")

        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
        ).stdout.decode()
        #
        # print('---------------------------')
        # print('outputs',output)
        # print('---------------------------')

        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        assert output.strip() == expected_out.strip()


def test_register3():
    """
    Boundary Value Robustness Testing
    Put a limit on username and password lengths: Will it crash?
    past 2000 characters each?
    Should pass constraints with failure on username length.
    """
    # Code to output big boundary test on username and password
    # fin = open("input_partition/test_register16.in", "w")
    # fin.write("2\n")
    # username = "a" * 2000
    # password = "G00dPassword!" * 154
    # fin.write("good.email15@gmail.com\n")
    # fin.write(username + '\n')
    # fin.write(password + '\n')
    # fin.write(password + '\n')
    # fin.close()

    str_in = "input_partition/test_register16.in"
    str_out = "input_partition/test_register16.out"
    expected_in = open(current_folder.joinpath(str_in))
    expected_out = open(current_folder.joinpath(str_out)).read()

    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()

    expected_out = expected_out.replace('\r', '')
    output = output.replace('\r', '')
    expected_out = expected_out.replace('\n', '')
    output = output.replace('\n', '')
    expected_out = expected_out.replace(' ', '')
    output = output.replace(' ', '')

    assert output.strip() == expected_out.strip()
