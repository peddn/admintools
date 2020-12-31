# admintools
Some python scripts to help automate a nginx, gunicorn, wagtail, postgresql stack.

## Notes
How to install multiple packages via textfile:
xargs -a ./install.txt sudo apt-get install -y

## Installation
You need a user allowed to execute sudo commands.
This software is designed to live in the system's global python environment.

```console
foo@bar:~$ sudo apt-get update
~$ sudo apt-get install build-essential
~$ git clone https://github.com/peddn/admintools.git
~$ cd admintools
~$ sudo pip install -r requirements.txt
~$ python3 admin.py --help
```