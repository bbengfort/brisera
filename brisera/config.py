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

    debug:        the app will print or log debug statements
    testing:      the app will not overwrite important resources
    max_chunk:    the maximum chunk of a sequence for mapping
    overlap:      the bp overlap to carry over in sequences
    min_read_len: the minimum length of the reads
    max_read_len: the maximum length of the reads
    k:            number of mismatches to allow (bigger means more time)
    allow_diff:   False is mismatches only, True indels as well
    filter_align: False uses all alignments, True only report unambiguous best alignment
    block_size:   number of qry and ref tuples to consider at a time in the reduce phase
    redundancy:   number of copies of low complexity seeds to use
    """

    CONF_PATHS = [
        "/etc/brisera.yaml",                      # System configuration
        os.path.expanduser("~/.brisera.yaml"),    # User specific config
        os.path.abspath("conf/brisera.yaml"),     # Local configuration
    ]

    debug        = True
    testing      = True
    max_chunk    = 65535
    overlap      = 1024  # ensure this is longer than longest read
    min_read_len = 36
    max_read_len = 36
    k            = 3
    allow_diff   = False
    filter_align = True
    block_size   = 128
    redundancy   = 16

    @property
    def seed_len(self):
        return self.min_read_len / (self.k+1)

    @property
    def flank_len(self):
        return self.max_read_len - self.seed_len + self.k

## Load settings immediately for import
settings = BriseraConfiguration.load()

if __name__ == '__main__':
    print settings
