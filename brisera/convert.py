"""
Handles the conversion of a FASTA sequence into a sequence format
"""

from brisera.utils import fasta
from brisera.config import settings

class FastaChunker(object):

    def __init__(self, path):
        self.path = path
        self.min_sequence_len = None
        self.max_sequence_len = None
        self.sequences = 0

    def chunk(self, sequence):
        """
        Chunks sequences and also records the min/max lengths.
        Yields a tuple as follows:
            0: the sequence chunk which is < settings.max_chunk
            1: the offset of the sequence from the original
            2: a boolean tag indicating a reference sequence (or last chunk)
        """

        length   = len(sequence)

        # Record the minimum and maximum sequence lengths
        if self.min_sequence_len is None or length < self.min_sequence_len:
            self.min_sequence_len = length

        if self.max_sequence_len is None or length > self.max_sequence_len:
            self.max_sequence_len = length

        # Alert if the sequence is large
        if length > 100:
            print "Large sequence discovered: %ibp" % length

        offset    = 0
        numchunks = 0

        while offset < length:
            numchunks += 1
            end = min(offset+settings.max_chunk, length)

            chunk = sequence[offset:end]
            yield (chunk, offset, end == length)

            if end == length:
                offset = length
            else:
                offset = end - settings.overlap

    def convert(self, writer):
        """
        The main entry point, convert the FASTA file and output it by
        writing it to the given stream (the writer).
        """

        for idx, seq in self:
            for chunk in self.chunk(seq):
                record = str((idx, chunk))
                writer.write(record+"\n")
                break
            break

    def __iter__(self):
        """
        Iterates over all the sequences using fasta reader and emits the
        1-indexed idx, sequence for each (omiting the label). Note that the
        sequence will be completely uppercase.
        """
        for label, sequence in fasta(self.path):
            self.sequences += 1 # Count the number of sequences
            yield (self.sequences, sequence.upper())

if __name__ == '__main__':
    import sys
    from brisera.utils import fixture
    path = fixture('100k.fa', 'cloudburst')
    chunker = FastaChunker(path)
    chunker.convert(sys.stdout)