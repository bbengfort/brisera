"""
Implements MerReduce alignment (seed-and-reduce) in a distributed fashion
"""

##########################################################################
## Imports
##########################################################################

from brisera.utils import *
from brisera.records import *
from brisera.config import settings
from brisera.exceptions import *

N = '.'

##########################################################################
## MerAlignment
##########################################################################

class MerAlignment(object):
    """
    Performs both map and reduce alignment akin to CloudBurst
    """

    def __init__(self, **kwargs):
        setting = lambda name: kwargs.get(name, getattr(settings, name))

        self.min_read_len = setting('min_read_len')
        self.max_read_len = setting('max_read_len')
        self.seed_len     = setting('seed_len')
        self.flank_len    = setting('flank_len')
        self.k            = setting('k')
        self.redundancy   = setting('redundancy')

    def parse_record(self, data):
        key, val = data     # Expand the key, value pair
        record     = deserialize_record(val)
        sequence   = record[0]
        offset     = record[1]
        is_last     = record[2]
        seqlen     = len(sequence)

        return key, sequence, offset, is_last, seqlen

    def map_reference(self, arg):
        """
        Input (id, (sequence, offset, tag))
        Yields tuples:
            (mer, (id, pos, tag, left, right, r))
        for each seed in the sequences that are passed in
        if tag = 0, also output the reverse complement sequences
        """

        key, sequence, offset, is_last, seqlen = self.parse_record(arg)

        start = 0
        if offset != 0:
            # Not the first chunk, shift for room on left flank
            start  = settings.overlap + 1 - self.flank_len - self.seed_len
            offset += start

        # stop so the last mer will fit
        end = seqlen - self.seed_len + 1

        if not is_last:
            # If not the last chunk, stop so the right flank fits as well
            end -= self.flank_len

        # Emit the mers starting at every position
        for idx in xrange(start, end):

            seed   = sequence[start:self.seed_len]
            if N in seed:
                continue

            offset += 1
            start  += 1

            leftstart = start - self.flank_len
            if leftstart < 0:
                leftstart = 0
            leftlen = start-leftstart

            rightstart = start + self.seed_len
            rightend   = rightstart + self.flank_len
            if rightend > seqlen:
                rightend = seqlen
            rightlen = rightend-rightstart

            seed = sequence[start:start+self.seed_len]
            if self.redundancy > 1 and repseed(sequence, start, self.seed_len):
                for rdx in xrange(self.redundancy):
                    r   = rdx % self.redundancy
                    yield (seed, (key, offset, is_last, leftstart, leftlen, rightstart, rightlen, r))
            else:
                yield (seed, (key, offset, is_last, leftstart, leftlen, rightstart, rightlen, 0))

    def map_queries(self, arg):
        """
        Input (id, (sequence, offset, tag))
        Yields tuples:
            (mer, (id, pos, tag, left, right, r))
        for each seed in the sequences that are passed in
        if tag = 0, also output the reverse complement sequences
        """
        key, sequence, offset, is_last, seqlen = self.parse_record(arg)

        if seqlen < self.min_read_len:
            raise ReadLengthException("read length %i < minimum read length %i", seqlen, self.min_read_len)
        elif seqlen > self.max_read_len:
            raise ReadLengthException("read length %i > maximum read length %i", seqlen, self.max_read_len)

        numN = sum(1 for char in sequence if char == N)

        for rc in xrange(2):

            if numN > self.k:
                break

            if rc == 1:
                # Reverse complement the sequence
                sequence = revc(sequence)
                is_rc = True
            else:
                is_rc = False

            # emit non-overlapping mers
            for idx in xrange(0, seqlen, self.seed_len):
                seed   = sequence[idx:idx+self.seed_len]
                if N in seed:
                    continue

                rightstart = idx+self.seed_len
                rightlen = seqlen - rightstart

                if self.redundancy > 1 and repseed(sequence, idx, self.seed_len):
                    r = key % self.redundancy
                    yield (seed, (key, idx, is_last, 0, idx, rightstart, rightlen, r))
                else:
                    yield (seed, (key, idx, is_last, 0, idx, rightstart, rightlen, 0))

##########################################################################
## Spark Functionality
##########################################################################

@timeit
def align_all(sc, refpath, qrypath):
    """
    Returns an RDD of alignments (no writes to disk)
    """
    reference = sc.sequenceFile(refpath)
    queries   = sc.sequenceFile(qrypath)
    alignment = MerAlignment()

    # Perform mapping
    reference = reference.flatMap(alignment.map_reference)
    return reference

if __name__ == '__main__':
    from brisera.convert import *
    # path = fixture('s_suis.fa', 'cloudburst')
    path = fixture('100k.fa', 'cloudburst')
    chunker = FastaChunker(path)
    aligner = MerAlignment()
    for chunk in chunker.convert():
        # for record in aligner.map_reference(chunk):
        for record in aligner.map_queries(chunk):
            print record
        # break
