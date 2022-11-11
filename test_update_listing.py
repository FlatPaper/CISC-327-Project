from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


for i in range(1, 12):

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_update_listing_'+str(i)+'.in'))
    expected_out = open(current_folder.joinpath(
        'test_update_listing_'+str(i)+'.out')).read()

    print(expected_out)


def test_login():
    """capsys -- object created by pytest to 
    capture stdout and stderr"""

    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()

    print('outputs', output)
    assert output.strip() == expected_out.strip() 
