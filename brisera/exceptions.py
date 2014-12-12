"""
Class hierarchy for exceptions in Brisera
"""

class BriseraException(Exception):
    """
    Top level class for Brisera exceptions
    """
    pass

class ImproperlyConfigured(BriseraException):
    """
    Something is wrong with a setting or configuration
    """
    pass

class ReadLengthException(BriseraException):
    """
    The read is not in bounds of the minimum and maximum read lengths
    """
    pass
