from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


def test_login():
    """capsys -- object created by pytest to 
    capture stdout and stderr"""
    
    for i in range(1, 12):

        # read expected in/out
        expected_in = open(current_folder.joinpath(
            'test_update_listing_'+str(i)+'.in'))
        expected_out = open(current_folder.joinpath(
            'test_update_listing_'+str(i)+'.out')).read()
    
        expected_out = expected_out.replace('\r', '')
        output = output.replace('\r', '')
        expected_out = expected_out.replace('\n', '')
        output = output.replace('\n', '')
        expected_out = expected_out.replace(' ', '')
        output = output.replace(' ', '')

        print(expected_out)

    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()

    print('outputs', output)
    assert output.strip() == expected_out.strip() 
