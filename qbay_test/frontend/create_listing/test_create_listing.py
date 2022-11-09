from os import popen
from pathlib import Path
import subprocess


def test_create_listing_input_partition():
    current_folder = Path(__file__).parent
    # All valid inputs for create listing
    expected_in = open(current_folder.joinpath('test1.in'))
    expected_out = open(current_folder.joinpath('test1.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Non Valid title
    expected_in = open(current_folder.joinpath('test2.in'))
    expected_out = open(current_folder.joinpath('test2.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Non valid description
    expected_in = open(current_folder.joinpath('test3.in'))
    expected_out = open(current_folder.joinpath('test3.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Non Valid Price
    expected_in = open(current_folder.joinpath('test4.in'))
    expected_out = open(current_folder.joinpath('test4.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b


def test_create_listing_output_exhaustive():
    current_folder = Path(__file__).parent
    # All valid inputs for create listing
    expected_in = open(current_folder.joinpath('test5.in'))
    expected_out = open(current_folder.joinpath('test5.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b

    # Title is not alphanumeric
    expected_in = open(current_folder.joinpath('test6.in'))
    expected_out = open(current_folder.joinpath('test6.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Title is greater than 80 characters
    expected_in = open(current_folder.joinpath('test7.in'))
    expected_out = open(current_folder.joinpath('test7.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Title has spaces at the end and start
    expected_in = open(current_folder.joinpath('test8.in'))
    expected_out = open(current_folder.joinpath('test8.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Description not between 20-2000 characters.
    expected_in = open(current_folder.joinpath('test9.in'))
    expected_out = open(current_folder.joinpath('test9.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Description not longer than the title.
    expected_in = open(current_folder.joinpath('test10.in'))
    expected_out = open(current_folder.joinpath('test10.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Price is not a number
    expected_in = open(current_folder.joinpath('test11.in'))
    expected_out = open(current_folder.joinpath('test11.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Price is not between 10-10000
    expected_in = open(current_folder.joinpath('test12.in'))
    expected_out = open(current_folder.joinpath('test12.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Shares title with another listing
    expected_in = open(current_folder.joinpath('test13.in'))
    expected_out = open(current_folder.joinpath('test13.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b


def test_create_listing_input_boundry():
    current_folder = Path(__file__).parent
    # All valid inputs for create listing
    expected_in = open(current_folder.joinpath('test14.in'))
    expected_out = open(current_folder.joinpath('test14.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b

    # Title is 80 characters
    expected_in = open(current_folder.joinpath('test15.in'))
    expected_out = open(current_folder.joinpath('test15.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Description is 20 charcters
    expected_in = open(current_folder.joinpath('test16.in'))
    expected_out = open(current_folder.joinpath('test16.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Description is 2000 chracters
    expected_in = open(current_folder.joinpath('test17.in'))
    expected_out = open(current_folder.joinpath('test17.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Title and Description are the same length
    expected_in = open(current_folder.joinpath('test18.in'))
    expected_out = open(current_folder.joinpath('test18.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Price is 10
    expected_in = open(current_folder.joinpath('test19.in'))
    expected_out = open(current_folder.joinpath('test19.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    # Price is 10000
    expected_in = open(current_folder.joinpath('test20.in'))
    expected_out = open(current_folder.joinpath('test20.out')).read()
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    a = "".join(str(expected_out).split())
    b = "".join(str(output).split())
    assert a == b
    