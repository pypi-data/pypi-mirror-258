'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the testing utility of StryPy.

First run this Python code on your command line or terminal::

    python3 -c "import strypy as sp; sp.copy(sp.get_test_path())"
    
Next navigate to that directory with the 'cd' command and pasted path::
    
    cd /paste/directory/here
    
Finally run pytest from that directory, which should be installed as a dependency of StryPy::
    
    pytest
    
These commands should work on all platforms.
'''

import strypy as sp

def get_test_path():
    '''
    Returns the tests directory path.
    
    >>> sp.get_test_path()
    '/path/to/tests/directory'
    '''
    
    path1 = sp.subtract(str(sp.__file__), 11)	# Removes __init__.py
    path = sp.add(path1, "tests")				# Adds tests directory
    return str(path)

# TODO: Create test() function which executes tests without having to type other commands, most likely using os.system() to run those commands.