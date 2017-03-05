LastPass Pwned Sites Checker
============================

Quick program based on
`lastpass-python <https://github.com/konomae/lastpass-python>`_
to check sites in the given LastPass account against a given plaintext file of
known "pwned" sites. If a match is found it is returned, leaving the user
to determine if the LastPass site entry should have its password changed, etc.

Install
-------

.. code-block:: bash

    $ git clone https://github.com/toozej/lastpass-pwned-checker.git
    $ cd lastpass-pwned-checker/
    $ # optionally create a virtual environment for Python with:
    $ # virtualenv venv && source venv/bin/activate
    $ pip install -r requirements.txt


Example Usage
-------------

.. code-block:: bash

    $ cp examples/credentials.json.example credentials.json
    $ # edit credentials.json with your LastPass credentials
    $ cp examples/pwned_list.txt pwned_list.txt
    $ # optionally get a new pwned list with
    $ # wget -O pwned_list.txt <some_site_with_pwned_list.com/list.txt>
    $ ./lppc > output.txt
    $ # sadly wait for a while, script is not multithreaded yet
    $ less output.txt # and take action on sites found if necessary
    $ # if you created venv, deactivate it


License
-------

`The MIT License <http://opensource.org/licenses/mit-license.php>`_

