"""
Utility functions for Brisera
"""

##########################################################################
## Imports
##########################################################################

import os
import time

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

def timeit(func):
    """
    Wrapper function for timing function calls
    """
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        finit  = time.time()
        delta  = finit-start
        return result, delta
    return wrapper

def revc(sequence):
    """
    Returns the complement of the DNA sequence
    """
    complements = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C',
        'N': 'N',
        '.': '.',
    }

    def inner(sequence):
        for char in reversed(sequence):
            yield complements[char]

    sequence = sequence.upper()
    return ''.join(inner(sequence))
