from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Utilities',
]
py_versions = ['2', '2.6', '2.7']
classifiers += ['Programming Language :: Python :: %s' % x for x in py_versions]


setup(
    name='bender',
    description='bender: general chat bot',
    version='0.1.0',
    url='https://github.com/bender-bot/bender',
    license='MIT license',
    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
    author='Fabio Menegazzo, Bruno Oliveira',
    author_email='menegazzo@gmail.com',
    classifiers=classifiers,
    # the following should be enabled for release
    install_requires=['futures', 'pyyaml'],
    packages=['bender', 'bender.backbones', 'bender.scripts'],
)

