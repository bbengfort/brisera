"""
Spark application that takes a FASTA file as input and outputs a binary
format that can quickly be read with Spark into an RDD.
"""

##########################################################################
## Imports
##########################################################################

import sys

from operator import add
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.stderr.write("Usage: convert_fasta.py input.fa output.br\n")
        sys.exit(-1)

    conf = SparkConf().setAppName("FASTA Conversion")
    sc   = SparkContext(conf=conf)

    infile  = sys.argv[1]
    outfile = sys.argv[2]

    print "Converting FASTA %s to Sequence %s" % (infile, outfile)


