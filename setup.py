#!/usr/bin/env python

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\". Please install the setuptools package.")


packages = find_packages(where=".", exclude=('tests', 'apps', 'docs', 'fixtures', 'conf', 'venv'))

requires = []

with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

classifiers = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Enivronment :: No Input/Output (Daemon)',
    'Environment :: MacOS X',
    'Intended Audience :: Science/Research',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
)

config = {
    "name": "brisera",
    "version": "1.0",
    "description": "A Python implementation of a distributed seed and reduce algorithm with Spark",
    "author": "Benjamin Bengfort",
    "author_email": "bengfort@cs.umd.edu",
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "zip_safe": False,
    "scripts": ["apps/convert_fasta.py"],
}

setup(**config)
