# admintools
Some python scripts to help automate a nginx, gunicorn, wagtail, postgresql stack.

TODO
====

installationsanleitungen

    * first time setup
    * nginx
    * djnago, postgresql, nginx, gunicorn

* basisabhängigkeiten sammeln

* installation in unabhängige abschnitte unterteilen

* diese abschnitte in tools umetzen

    * first time setup
    * update



How to install multiple packages via textfile:
xargs -a ./install.txt sudo apt-get install -y



INSTALLATION
============

You need a user allowed to execute sudo commands.
This software is designed to live in the system's global python environment.

~$ sudo apt-get update
~$ sudo apt-get install build-essential
~$ git clone https://github.com/peddn/admintools.git
~$ cd admintools
~$ sudo pip install -r requirements.txt
~$ python3 admin.py --help
