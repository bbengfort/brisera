"""
Spark application that reads a CloudBurst sequence file and converts it
into text for review and analysis.
"""

##########################################################################
## Imports
##########################################################################

import sys

from brisera.records import record_from_bytes
from pyspark import SparkConf, SparkContext

PROG_NAME = "read_burst.py"
APP_NAME  = "CloudBurst Reader"

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s sequences.br output\n" % PROG_NAME)
        sys.exit(-1)

    conf = SparkConf().setAppName(APP_NAME)
    sc   = SparkContext(conf=conf)

    infile  = sys.argv[1]
    outpath = sys.argv[2]

    print "Converting Sequence File %s to Text using directory %s" % (infile, outpath)

    sequences = sc.sequenceFile(infile)
    sequences = sequences.map(lambda (k,v): (k, record_from_bytes(v)))
    sequences.saveAsTextFile(outpath)


