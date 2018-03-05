# -*- coding: utf-8 -*-

from setuptools import setup

# 2018-03-04 (tonyc) this breaks because it imports urwid, which the user may
# or may not have installed yet.  For now, just maintain README separately.

#import urwid_utils

# README.rst dynamically generated:
# with open('README.rst', 'w') as f:
#     f.write(urwid_utils.__doc__)

NAME = "urwid_utils" #urwid_utils.__name__

def read(file):
    with open(file, 'r') as f:
        return f.read().strip()

setup(
    name=NAME,
    version=read('VERSION'),
    description='A collection of simple, straightforward, but extensible utilities for the urwid package.',
    # long_description=read('README.rst'),
    author='Tony Cebzanov',
    author_email='tonycpsu@gmail.com',
    url='https://github.com/stnbu/{0}'.format(NAME),
    download_url='https://github.com/tonycpsu/{0}/archive/master.zip'.format(NAME),
    provides=[NAME],
    install_requires=['urwid'],
    license='MIT',
    bugtrack_url='https://github.com/tonycpsu/{0}/issues'.format(NAME),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    packages=[NAME],
    keywords=[],
    test_suite='test',
)
