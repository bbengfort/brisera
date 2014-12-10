"""
Utility functions for Brisera
"""

##########################################################################
## Imports
##########################################################################

import os

##########################################################################
## Module Constants
##########################################################################

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXTURES = os.path.join(BASE_DIR, "fixtures")

##########################################################################
## Utility Functions
##########################################################################

def fixture(fname, label="reference"):
    """
    Returns a path to a fixture via the given fname and label
    """
    return os.path.join(FIXTURES, label, fname)

def fasta(path):
    """
    Reads a file in FASTA format, returning a tuple, (label, sequence).
    """
    label    = None
    sequence = None
    with open(path, 'r') as data:
        for line in data:
            line = line.strip()
            if line.startswith('>'):
                if label and sequence:
                    yield (label, sequence)
                label = line[1:]
                sequence = ""
            else:
                sequence += line

        if label and sequence:
            yield (label, sequence)
