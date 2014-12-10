"""
Uses confire to get meaningful configurations from a yaml file
"""

##########################################################################
## Imports
##########################################################################

import os
import confire

##########################################################################
## Configuration
##########################################################################

class BriseraConfiguration(confire.Configuration):
    """
    Meaningful defaults and required configurations.

    debug:    the app will print or log debug statements
    testing:  the app will not overwrite important resources
    """

    CONF_PATHS = [
        "/etc/brisera.yaml",                      # System configuration
        os.path.expanduser("~/.brisera.yaml"),    # User specific config
        os.path.abspath("conf/brisera.yaml"),     # Local configuration
    ]

    debug    = True
    testing  = True


## Load settings immediately for import
settings = BriseraConfiguration.load()

if __name__ == '__main__':
    print settings
