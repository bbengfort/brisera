"""
Utilities to help create and serialize records in binary format
"""

##########################################################################
## Imports
##########################################################################

import cPickle

##########################################################################
## Module Constants
##########################################################################

DNA_BYTES = {
    'A': 0x00,
    'C': 0x01,
    'G': 0x02,
    'T': 0x04,
    'N': 0x08,
    'space': 0x0F,
    'hardstop': 0xFF,
}

BYTES_DNA = dict((v, k) for (k,v) in DNA_BYTES.items())

##########################################################################
## Helper functions
##########################################################################

def dna_from_seq(dna, pos, length):
    if length == 0:
        return ""

    alen = 2 * length
    end  = pos + length - 1

    if (dna[end] & 0x0F) == DNA_BYTES['space']:
        alen -= 1

    idx = 0
    arr = [""] * alen

    while pos < end:
        arr[idx]   = (dna[pos] & 0xF0) >> 4
        arr[idx+1] = (dna[pos] & 0x0F)

        pos += 1
        idx += 2

    arr[idx] = (dna[pos] & 0xF0) >> 4
    idx += 1

    if (dna[pos] & 0x0F) != DNA_BYTES['space']:
        arr[idx] = dna[pos] & 0x0F

    string = ""
    for b in arr:
        string += BYTES_DNA[b]

    return string

def repseed(seq, start, slen):
    first = seq[start]
    for idx in xrange(slen):
        if seq[idx+start] != first:
            return False
    return True

def record_from_bytes(raw):

    last_chunk = raw[0] == 1
    offset = (
        (raw[1] & 0xFF) << 24 |
        (raw[2] & 0xFF) << 16 |
        (raw[3] & 0xFF) << 8  |
         raw[4] & 0xFF
    )
    sequence = dna_from_seq(raw, 5, len(raw)-5)

    return sequence, offset, last_chunk

def serialize_record(record):
    """
    Convert a tuple into a binary string for use with SequenceFiles
    """
    return cPickle.dumps(record, 0)

def deserialize_record(record):
    """
    Read a binary record object and return the tuple
    """
    record = record.encode('utf-8')
    return cPickle.loads(record)

if __name__ == '__main__':
    value = bytearray(b'\x01\x00\x00\x00\x00!\x14$AD@\x10B\x04DD"A@$$\x04"')
    print record_from_bytes(value)
