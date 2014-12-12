"""
Basic implementation of Landau-Viskin for alignments
"""

##########################################################################
## Imports
##########################################################################

import sys
from numpy import zeros

##########################################################################
## Module Constants
##########################################################################

NO_ALIGNMENT  = ( 0, 0,None,None,0)
BAD_ALIGNMENT = (-1,-1,None,None,0)

class LandauVishkin(object):

    def __init__(self):
        self.L    = None
        self.B    = None
        self.dist = None
        self.what = None

    def configure(self, k):
        self.L = zeros((k*2+1, k+1), dtype=int)
        self.B = zeros((k*2+1, k+1), dtype=int)
        self.dist = zeros(k+1, dtype=int)
        self.what = zeros(k+1, dtype=int)

    def kmismatch(self, text, pattern, k):
        self.configure(k)
        m = len(pattern)
        n = len(text)

        if m == 0 or n == 0:
            return NO_ALIGNMENT

        last  = m if m < n else n
        mm    = 0
        match = 0

        for pos in xrange(last):
            if text[pos] != pattern[pos]:
                self.what[mm] = 0
                self.dist[mm] = match
                match = 0

                mm += 1

                if mm > k:
                    return BAD_ALIGNMENT
            match += 1

        self.dist[mm] = match
        self.what[mm] = 2

        return (last, mm, self.dist, self.what, mm+1)

    def kdifference(self, text, pattern, k):
        self.configure(k)
        m = len(pattern)
        n = len(text)

        if m == 0 or n == 0:
            return NO_ALIGNMENT

        # Compute via dynamic programming
        for e in xrange(k+1):
            for d in xrange(-e, e):
                row = -1

                if e > 0:
                    if abs(d) < e:
                        up = self.L[k+d][e-1] + 1
                        if up > row:
                            row = up
                            self.B[k+d][e] = 0

                    if d > -(e-1):
                        left = self.L[k+d-1][e-1]
                        if left > row:
                            row = left
                            self.B[k+d][e] = -1

                    if d < (e-1):
                        right = self.L[k+d+1][e-1]+1
                        if right > row:
                            row = right
                            self.B[k+d][e] = 1
                else:
                    row = 0

                while ((row < m) and (row+d < n) and (pattern[row] == text[row+d])):
                    row += 1

                self.L[k+d][e] = row

                if (row+d == n) or (row == m):
                    # reached the end of the pattern or text
                    distlen = e+1

                    E = e
                    D = d

                    self.what[E] = 2

                    while e >= 0:
                        b = self.B[k+d][e]
                        if e > 0:
                            self.what[e-1] = b

                        self.dist[e] = self.L[k+d][e]

                        if e < E:
                            self.dist[e+1] -= self.dist[e]

                        d += b
                        e -= 1

                    return (row+D, E, self.dist, self.what, distlen)

        # How did we get here?
        raise TypeError("Unexpected end of dynamic programming")

##########################################################################
## Helper functions for alignments
##########################################################################

def is_bazea_yates_seed(alignment, qlen, kmerlen):
    # Since an alignment may be recompute k+1 times for each of the k+1 seeds,
    # see if the current alignment is the leftmost alignment by checking for
    # differences in the proceeding chunks of the query

    alignlen, differences, dist, what, distlen = alignment
    num_buckets = qlen / kmerlen
    lastbucket = -1
    distdelta  = 0
    pos        = 0

    for idx in xrange(distlen):
        pos += dist[idx] + distdelta
        distdelta = 0

        if what[idx] == 2:
            continue # end of string
        elif what[idx] == -1:
            # gap character occurs
            if pos % kmerlen == 0:
                continue # occurs between buckets, skip

        bucket = pos / kmerlen
        if (bucket - lastbucket) > 1:
            return False
        lastbucket = bucket

    return lastbucket == (num_buckets-1)

def str_alignment(alignment):
    alignlen, differences, dist, what, distlen = alignment
    astr = "%i;%i;" % (alignlen, differences)
    astr += ";".join("%i" % i for i in dist)
    astr += ";"
    astr += ";".join("%i" % i for i in what)
    astr += ";"
    return astr

def print_alignment(alignment, t, p):
    alignlen, differences, dist, what, distlen = alignment

    if dist is None:
        sys.stdout.write("t: %s" % text)
    else:
        sys.stdout.write("a: ")
        nextstride = 0
        for idx in xrange(distlen):
            if what[idx] == 2:
                break
            stride = dist[idx] + nextstride
            for jdx in xrange(stride):
                sys.stdout.write(" ")
            sys.stdout.write("*")

            nextstride = 0
            if what[idx] == 1 or what[idx] == 0:
                nextstride = -1
        sys.stdout.write("\n")

        sys.stdout.write("t: ")
        pos = 0
        nextstride = 0
        for idx in xrange(distlen):
            stride = dist[idx] + nextstride

            nextstride = -1 if what[idx] == 1 else 0

            for jdx in xrange(stride):
                sys.stdout.write(t[pos])
                pos += 1

            if what[idx] == 1:
                sys.stdout.write('-')
            elif what[idx] == -1:
                sys.stdout.write(t[pos])
                pos += 1

    sys.stdout.write("\np: ")

    if dist is None:
        sys.stdout.write(p)
    else:
        pos = 0
        for idx in xrange(distlen):
            for jdx in xrange(dist[idx]):
                sys.stdout.write(p[pos])
                pos += 1

            if what[idx] == -1:
                sys.stdout.write("-")

    sys.stdout.write("\n")

def check_bys(k, t, p, shouldbeseed, name, kmerlen):
    print "checking %s (%s)" % (name, shouldbeseed)

    if len(p) != 10:
        raise ValueError("Read length incorrect: %i" % len(p))

    lv = LandauVishkin()
    a = lv.kdifference(t,p,k)
    print_alignment(a,t,p)

    if is_bazea_yates_seed(a, len(p), kmerlen) != shouldbeseed:
        print "should match!"

    print

if __name__ == '__main__':
    k = 5
    lv = LandauVishkin()
    text    = "TTTCTCAAACACCTATATTTTTTGT"
    pattern = "TTTCTCAAACACCTATATTTTTT"

    align = lv.kdifference(text, pattern, k)
    print "ASCII: %s" % str_alignment(align)
    print_alignment(align, text, pattern)


    # Check BY seeds
    k = 3
    KMER_LEN = 5

    t = "AACCGATTCCCAA"

    check_bys(k, t, "AACCGATTCC", False, "exact", KMER_LEN);

    check_bys(k, t, "ACCCGATTCC", False, "1-mismatch", KMER_LEN);
    check_bys(k, t, "ACCGATTCCC", False, "1-del", KMER_LEN);
    check_bys(k, t, "AAACCGATTC", False, "1-ins", KMER_LEN);

    check_bys(k, t, "AACCGATCCC", False, "2-mismatch", KMER_LEN);
    check_bys(k, t, "AACCGTTCCC", False, "2-del", KMER_LEN);
    check_bys(k, t, "AACCGATTTC", False, "2-ins", KMER_LEN);

    check_bys(k, t, "ACCCGATCCC", True,  "1-mis, 2-mis", KMER_LEN);
    check_bys(k, t, "ATCCGATTCA", True,  "1-mis, 2-del", KMER_LEN);
    check_bys(k, t, "ATCCGATTTC", True,  "1-mis, 2-ins", KMER_LEN);

    check_bys(k, t, "ACCGATACCC", True,  "1-del, 2-mis", KMER_LEN);
    check_bys(k, t, "ACCGATCCCA", True,  "1-del, 2-del", KMER_LEN);
    check_bys(k, t, "ACCGATTTCC", True,  "1-del, 2-ins", KMER_LEN);

    check_bys(k, t, "TACCGTTCCA", True,  "1 del boundary", KMER_LEN);
    check_bys(k, t, "AACCGTCCCA", False, "1 del boundary", KMER_LEN);
    check_bys(k, t, "AACCGCCCAA", False, "1 del boundary", KMER_LEN);
