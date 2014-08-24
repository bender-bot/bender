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

**Note**: If you are on windows, you have to install python (or symlink to it) in 
`C:\PythonXY`, where `XY` is the main python version, so `C:\Python27`, 
`C:\Python34`, and so on.   