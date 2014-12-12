"""
Spark application that takes a preprocessed query file and DNA sequence
and uses seed-and-reduce (e.g. BLAST) to find alignments in a distributed
fashion (similar to CloudBurst's implementation on Hadoop).

Spark implements RDDs - an efficient way of cacheing repeated data in
memory, saving some of the overhead of disk IO that is requied in Hadoop,
as such, Spark is a much faster processing platform for distributed
alignments than Hadoop and Cloudburst.
"""

##########################################################################
## Imports
##########################################################################

import sys
import brisera

from brisera.utils import timeit
from brisera.config import settings
from pyspark import SparkConf, SparkContext

@timeit
def run_brisera_alignment(sc, refpath, qrypath, outpath):
    """
    Runs the complete alignment
    """
    # Execute the alignments
    alignments, adelta = brisera.align_all(sc, refpath, qrypath)

    # Filter best alignments
    if settings.filter_align:
        alignments, fdelta = brisera.filter_alignments(sc, alignments)
    else:
        fdelta = 0

    # Write alignments to disk
    alignments.saveAsTextFile(outpath)

    return alignments, adelta, fdelta

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.stderr.write("Usage: convert_fasta.py refpath qrypath outpath\n")
        sys.stderr.write("    all other settings are stored in brisera.yaml\n")
        sys.exit(-1)

    conf = SparkConf().setAppName("Brisera Alignment")
    sc   = SparkContext(conf=conf)

    refpath = sys.argv[1]
    qrypath = sys.argv[2]
    outpath = sys.argv[3]

    if settings.redundancy < 1:
        raise brisera.ImproperlyConfigured("Minimum redundancy is 1")

    if settings.max_read_len > settings.overlap:
        raise brisera.ImproperlyConfigured("Increase overlap for %i length reads"
            " and reconvert FASTA file.", settings.max_read_len)

    result, delta = run_brisera_alignment(sc, refpath, qrypath, outpath)
    alignments, adelta, fdelta = result
    print "Total execution time: %0.3f seconds" % delta
    print "    Alignment time: %0.3f seconds" % adelta
    print "    Filtering time: %0.3f seconds" % fdelta
