# bender #

Your friendly generic chat bot.


## Developing ##

Testing is done with [pytest](http://pytest.org/latest/) and 
[tox](http://tox.readthedocs.org/en/latest/).

To run the tests:

```bash
$ virtualenv .env
$ source .env/bin/activate # or .env27\Scripts\activate.bat on Windows
$ pip install tox
$ tox
```