"""
GenomicRangeQuery

Find the minimal nucleotide from a range of sequence DNA

https://codility.com/programmers/task/genomic_range_query/

This is a fairly straightforward problem: you can go through every query and pull out the sliced sequence, then
  inspect the sequence for the minimal-factor.  Taking advantage of the fact the minimal factor values correspond to
  alphabetical order, sorting the slice into alphabetical order puts the minimum factor magically at the front
  of the string. Map it to the value and you're done. Yes?  See 'slow_solution' below.

No. Not done.

The straightforward solution visits every nucleotide in every slice. If the slices overlap a lot, then
  the solution revisits the same nucleotide multiple times.  If you could arrange the solution to
  only visit each nucleotide once, then it would be substantially faster.

But how?

We need to pass over the sequence and produce an intermediatory data structure which compiles the data we
need so we can access it directly; that is, without stepping through any part of the sequence again.

Enter the "prefix sum" pattern.

In this problem, we create an array for each type of item then, at each step through the sequence, record
 the count of how many of each type we've seen.  When we're done, for the example sequence
 "CAGCCTA", we finish up with:

    sumA = [0,0,1,1,1,1,1,2]
    sumC = [0,1,1,1,2,3,3,3]
    sumG = [0,0,0,1,1,1,1,1]
    sumT = [0,0,0,0,0,0,1,1]

Now when we can ask "Are there any 'C' types between points 2 and 4?" we can lookup sumC for the answer:
  At point 2 we had seen "1" type C nucleo, and at point 4 we'd seen 2. Thus, we can establish that
  there is exactly 1 (2-1).

So with this approach we can go through all the queries plugging in the start and end indexes and comparing
the results.  This will tell us which nucleotides appear in each query and thence determine the 'minimum impact'.
"""
import unittest
import random

# maximum number of neucleotides in a sequence
MAX_N = 100000
# maximum number of queries
MAX_M = 50000

# impact factor of each neucleotide
M = {'A': 1, 'C': 2, 'G': 3, 'T': 4}


def slow_solution(S, P, Q):
    """
    An easy to implement and understand solution: O(N * M)

    :param S: a string of 1..MAX_N chars containing a mix of the four chars A, C, G, and T
    :param P: a list of integers indexing a position in S
    :param Q: a list of integers indexing a position in S
    :return: a list of ints between 1 and 4, one for each query

    https://codility.com/demo/results/trainingC9QT9A-BQS/
    """
    # for every query, sort the sequence slice into alphabetical order: the first char will be the minimal-factor
    result = []
    for p, q in zip(P, Q):
        slice = sorted(S[p:q+1])
        result.append(M[slice[0]])
    return result


def fast_solution(S, P, Q):
    """
    A faster, but more difficult to implement and understand, solution: 0(N + M)

    :param S: a string of 1..MAX_N chars containing a mix of the four chars A, C, G, and T
    :param P: a list of integers indexing a position in S
    :param Q: a list of integers indexing a position in S
    :return: a list of ints between 1 and 4, one for each query

    https://codility.com/demo/results/trainingH6PA4P-5V7/
    """
    # Pass 1: Create suffix sums
    # We build four lists, one for each nucleo, which are as long as the sequence itself (plus one).
    # The lists preserve the sequence order and track the sum total of how many times we've seen that
    # nucleo type as we progress through the list.
    # Eg: The sum for "C" in "CAGCCTA" are [0,1,1,1,2,3,3,3]
    sumA = [0]; sumC = [0]; sumG = [0]; sumT = [0]
    for nuke in S:
        for sum in (sumA, sumC, sumG, sumT):
            sum.append(sum[-1])
        if nuke == 'A':
            sumA[-1] += 1
        elif nuke == 'C':
            sumC[-1] += 1
        elif nuke == 'G':
            sumG[-1] += 1
        else:
            sumT[-1] += 1

    # Pass 2: Evaluate the queries
    # Each query defines a slice via indicies P and Q which correspond to the start and end points.
    # By comparing the sum at both points we can readily determine how many nucleos of that type
    # appear within them.
    # Eg: In the sum [0,1,1,1,2,3,3,3], at index 2 there is a 1, and at index 4, there is a 2.
    # Thus, somewhere between indexes 2 and 4, there must have been a nucleo of type 'C'.
    # Additionally, we can determine how many 'C' nucleos are there by subtracting one sum from the other (2-1=1).
    impact = []
    for p, q in zip(P, Q):
        if sumA[q+1] > sumA[p]:
            impact.append(M['A'])
        elif sumC[q+1] > sumC[p]:
            impact.append(M['C'])
        elif sumG[q + 1] > sumG[p]:
            impact.append(M['G'])
        else:
            impact.append(M['T'])
    return impact


solution = fast_solution


class TestExercise(unittest.TestCase):
    def test_example(self):
        self.assertEqual(solution('CAGCCTA', [2,5,0], [4,5,6]), [2, 4, 1])

    def test_random(self):
        seq = [random.choice("ACGT") for _ in xrange(1, 5000)]
        P_array, Q_array = [], []
        for _ in xrange(0, len(seq)):
            P = random.randint(0, len(seq)-1)
            Q = random.randint(P, len(seq)-1)
            P_array.append(P)
            Q_array.append(Q)
        solution(seq, P_array, Q_array)

    def test_extreme(self):
        S = 'T' * MAX_N
        P = [0] * MAX_M
        Q = [MAX_N - 1] * MAX_M
        self.assertEqual(solution(S, P, Q), [4] * MAX_M)

if __name__ == '__main__':
    unittest.main()
