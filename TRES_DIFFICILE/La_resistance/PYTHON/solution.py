__author__ = 'latty'

import sys
import math

import bisect


# url:
# http://stackoverflow.com/questions/7380629/perform-a-binary-search-for-a-string-prefix-in-python
class PrefixCompares(object):

    def __init__(self, value=None):
        self.value = value

    def __lt__(self, other):
        return self.value < other[0:len(self.value)]

    def __gt__(self, other):
        return self.value[0:len(self.value)] > other

# url:
# stackoverflow.com/questions/7380629/perform-a-binary-search-for-a-string-prefix-in-python
def bisect_right_prefix(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid] and not a[mid].startswith(x):
            hi = mid
        else:
            lo = mid + 1
    return lo

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# dictionnaire de conversion ASCII -> MORSE
ascii_morse_mapping = {
    'A': '.-', 'B': '-...', 'C': '-.-.',
    'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..'
}

seq = raw_input()

n = int(raw_input())
list_w = []
for i in xrange(n):
    w = raw_input()
    #
    list_w.append(''.join([ascii_morse_mapping[char] for char in w]))

# tri de la liste des mots pour utilisation (future) du module bisect
list_w.sort()


def recursive_solve(sequence, list_words):
    ''' '''
    possibilities_memory = {}
    set_size = set([len(w) for w in list_words])

    def possibilities(beg, end):
        seq = sequence[beg:end]
        #
        if len(seq) == 0:
            return 1

        tuple_seq = (beg, end)
        if tuple_seq in possibilities_memory:
            return possibilities_memory[tuple_seq]

        total = 0
        #
        for size_prefix in filter(lambda x: x <= len(seq), set_size):
            prefix = seq[:size_prefix]
            leftIndex = bisect.bisect_left(list_words, prefix)
            rightIndex = bisect_right_prefix(list_words, prefix)
            count = len(
                filter(
                    lambda w: len(w) == size_prefix,
                    list_words[leftIndex:rightIndex]
                    )
                )
            if count > 0:
                total += count * possibilities(beg + size_prefix, end)
        #
        possibilities_memory[tuple_seq] = total

        return total

    return possibilities(0, len(sequence))

'''
def iter_solve(seq, list_words):
    #print >> sys.stderr, "seq: ", seq
    #print >> sys.stderr, "list_words: ", list_words
    #
    possibilities_memory = {}
    #
    total = 0
    #
    min_size = len(min(list_words, key=lambda w: len(w)))
    max_size = len(max(list_words, key=lambda w: len(w)))
    min_for_seq = min_size
    #
    key = PrefixCompares()
    begin = 0
    end = len(seq)
    list_seqs_to_test = [(seq, '', 0)]
    while list_seqs_to_test:
        print >> sys.stderr, "-> ", len(list_seqs_to_test)
        cur_seq, cur_path, cur_total = list_seqs_to_test.pop(0)
        if len(cur_seq) == 0:
            possibilities_memory[cur_path] = cur_total + 1
            total += cur_total + 1
        else:
            if cur_seq in possibilities_memory:
                possibilities_memory[cur_path + cur_seq] = cur_total
                total += cur_total + possibilities_memory[cur_path]
            else:
                max_for_seq = min(max_size, len(cur_seq))
                for size_prefix in range(min_for_seq, max_for_seq + 1):
                    prefix = cur_seq[:size_prefix]
                    #print >> sys.stderr, "prefix: ", prefix
                    key.value = prefix
                    leftIndex = bisect.bisect_left(list_words, key)
                    rightIndex = bisect.bisect_right(list_words, key)
                    count = len(
                        filter(lambda w: w == prefix, list_words[leftIndex:rightIndex]))
                    #print >> sys.stderr, "count: ", count
                    if count > 0:
                        #print >> sys.stderr, "-> ", (cur_seq[size_prefix:], cur_path + prefix, count + cur_total)
                        list_seqs_to_test.append(
                            (cur_seq[size_prefix:], cur_path + prefix, cur_total))
    return total
'''

# print iter_solve(seq, list_w)
print recursive_solve(seq, list_w)
