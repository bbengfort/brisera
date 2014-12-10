"""
Initialization test for the Brisera testing library
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## TestCases
##########################################################################

class InitializationTests(unittest.TestCase):

    def test_sanity(self):
        """
        Assert the world is sane and 2+2 = 4
        """
        self.assertEqual(2+2, 4)

    def test_import(self):
        """
        Assert that we can import the brisera module
        """
        try:
            import brisera
        except ImportError:
            self.fail("could not import brisera")
