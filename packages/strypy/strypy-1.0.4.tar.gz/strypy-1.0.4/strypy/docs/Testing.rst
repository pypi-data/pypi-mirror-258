=======
Testing
=======

StryPy comes with a whole set of assertion tests for all functions and can be run by the user once the package is installed.
`pytest <https://pytest.org>`_ is used for this.

**First run this Python code on your command line or terminal**::

    python3 -c "import strypy as sp; sp.copy(sp.get_test_path())"
    
**Next open up your command line and navigate to that directory with the 'cd' command and pasted path**::
    
    cd /paste/directory/here
    
**Finally run pytest from that directory, which should be installed as a dependency of StryPy**::
    
    pytest
    
These commands should work on all platforms. If any errors are raised from the testing result or when executing commands please create a new issue at https://github.com/TomTheCodingGuy/StryPy/issues describing it.