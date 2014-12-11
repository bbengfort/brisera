"""
Spark application that takes a FASTA file as input and outputs a binary
format that can quickly be read with Spark into an RDD.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import shutil
import tempfile

from brisera.convert import FastaChunker
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.stderr.write("Usage: convert_fasta.py input.fa output.br\n")
        sys.exit(-1)

    conf = SparkConf().setAppName("FASTA Conversion")
    sc   = SparkContext(conf=conf)

    infile  = sys.argv[1]
    outfile = sys.argv[2]
    tempdir = tempfile.mkdtemp(prefix="fasta")
    tempout = os.path.join(tempdir, "output")

    print "Converting FASTA %s to Sequence %s" % (infile, outfile)

    chunker = FastaChunker(infile)
    chunks  = sc.parallelize(chunker.convert()).coalesce(1, shuffle=True)
    chunks.saveAsSequenceFile(tempout)

    partfile = None
    for name in os.listdir(tempout):
        if name.startswith('part-'):
            partfile = os.path.join(tempout, name)
            break

    if partfile is None:
        raise Exception("Could not find partition file in %s!" % tempout)

    shutil.move(partfile, outfile)
    shutil.rmtree(tempdir)

    assert not os.path.exists(tempdir)
