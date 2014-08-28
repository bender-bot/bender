import sys

from setuptools import setup


classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Utilities',
]
py_versions = ['2', '2.6', '2.7', '3.4']
classifiers += [
    'Programming Language :: Python :: %s' % x
    for x in py_versions
]

requirements = ['pyyaml']
if sys.version_info[:2] < (3, 2):
    requirements += ['futures']

setup(
    name='bender',
    description='bender: general chat bot',
    version='0.1.0',
    url='https://github.com/bender-bot/bender',
    license='LGPLv3',
    platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
    author='Fabio Menegazzo <menegazzo@gmail.com>, Bruno Oliveira <nicoddemus@gmail.com>',
    classifiers=classifiers,
    install_requires=requirements,
    packages=['bender', 'bender.backbones', 'bender.scripts'],
    entry_points={
        'console_scripts': [
            'bender = bender._main:main',
        ],
        'pytest11': ['pytest-bender = bender.testing']
    }
)
