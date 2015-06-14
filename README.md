Brisera
=======

A Python implementation of a distributed seed and reduce algorithm (similar to BlastReduce and CloudBurst) that utilizes RDDs (resilient distributed datasets) to perform fast iterative analyses and dynamic programming without relying on chained MapReduce jobs.

Quick Start
-----------

The code is organized as follows:

- `apps/` - this directory contains the SparkApplications to be run
- `brisera/` - this is the python module with the code
- `tests/` - contains a stub testing library for ensuring things work
- `fixtures/` - contains reference data for running the apps against
- `docs/` - stubs for documentation for the project

To install the required dependencies:

    $ pip install -r requirements.txt

The code for Brisera is found in the `brisera` Python module. This module must be available to the spark applications (e.g. able to be imported) either by running the spark applications locally in the working directory that contains `brisera` or by using a virtual environment (recommended). You can install `brisera` and all dependencies, use the setup.py function:

    $ python setup.py install

But note that you will still have to have access to the Spark applications that are in the `apps/` directory - don't delete them out of hand!

Usage
-----

To read a burst sequence file (e.g. `fixtures/cloudburst/100k.br`) in order to compare results from CloudBurst to Brisera, you can use the `read_burst.py` Spark application as follows:

    $ spark-submit --master local[*] apps/read_burst.py <sequence_file> <output_dir>

This will write out each record (or chunk) from the sequence file to a text file on disk.

To convert a FASTA file for use with Brisera alignments, you can use the `convert_fasta.py` Spark application as follows:

    $ spark-submit --master local[*] apps/convert_fasta.py input.fa output.ser

This command will transform a single FASTA file into a chunked, binary format that can be used with Spark in a computationally efficient way (preparing the chunks for seed reduce).

To compute alignments, use the `brisera_align.py` Spark application. Note that this application takes its configuration from the `conf/brisera.yaml` file, an example of which is included. You can modify the configuration for the app by modifying that file. Run the alignment as follows:

    $ spark-submit --master local[*] apps/brisera_align.py refpath qrypath outpath

The input is as follows:

- The `refpath` is the converted FASTA file of the reference genome you wish to align to
- The `qrypath` is the set of queries or reads that you would like aligned to the reference
- The `outpath` is where the alignment information will be written to when complete

Depending on the value you set for K, this could take seconds to hours; be aware of how modifying the settings can change things!

Other Details
-------------

Brisera means to "explode" or to "burst" in Swedish. Since I'm reworking CloudBurst and BlastReduce (both of which use BLAST) to Spark (weirdly all the same terminology) it felt right to name the project something burst/explode related. (I tried a few languages, but Swedish had the best result).

### References

1. M\. C. Schatz, “BlastReduce: high performance short read mapping with MapReduce,” University of Maryland, [http://cgis. cs.umd.edu/Grad/scholarlypapers/papers/MichaelSchatz](http://cgis. cs.umd.edu/Grad/scholarlypapers/papers/MichaelSchatz). pd f, 2008.

1. M\. C. Schatz, “CloudBurst: highly sensitive read mapping with MapReduce,” Bioinformatics, vol. 25, no. 11, pp. 1363–1369, 2009.

1. X\. Li, W. Jiang, Y. Jiang, and Q. Zou, “Hadoop Applications in Bioinformatics,” in Open Cirrus Summit (OCS), 2012 Seventh, 2012, pp. 48–52.

1. R\. K. Menon, G. P. Bhat, and M. C. Schatz, “Rapid parallel genome indexing with MapReduce,” in Proceedings of the second international workshop on MapReduce and its applications, 2011, pp. 51–58.
