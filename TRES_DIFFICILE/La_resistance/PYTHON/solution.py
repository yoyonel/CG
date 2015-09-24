__author__ = 'latty'

import sys
import math

CODE = {
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

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l = raw_input()

n = int(raw_input())
list_w = []
for i in xrange(n):
    w = raw_input()
    #
    list_w.append(''.join([CODE[char] for char in w]))

list_w.sort()
print >> sys.stderr, "list_w: ", list_w
print >> sys.stderr, "l:", l
nb_w_found = 0
offset = 0
list_results = []
list_search_w = [(0, 0, list_w, 0)]
while list_search_w:
    #print >> sys.stderr, "list_search_w:", list_search_w
    #
    new_list_search_w = []
    for offset_l, offset_w, list_rest_w, nb_w_found in list_search_w:
        #print >> sys.stderr, "offset_l, offset_w, list_rest_w, nb_w_found:",offset_l, offset_w, list_rest_w, nb_w_found
        char = l[offset_l]
        list_w_for_char = filter(lambda x: x[offset_w] == char, list_rest_w)
        #print >> sys.stderr, "list_w_for_char :", list_w_for_char
        #
        #
        list_w_ending = filter(lambda x: len(x) == (offset_w+1), list_w_for_char)
        #print >> sys.stderr, "offset_w:", offset_w
        #print >> sys.stderr, "list_w_for_char:", list_w_for_char
        #print >> sys.stderr, "list_w_ending:", list_w_ending
        for w in list_w_ending:
            new_offset_l = offset_l + 1
            if new_offset_l < len(l):
                new_list_search_w.append(
                    (
                        offset_l + 1,
                        0,
                        list_w,
                        nb_w_found + 1
                    )
                )
            else:
                list_results.append(nb_w_found+1)
                print >> sys.stderr, "**** list_results:", list_results

        list_w_not_ending = filter(lambda x: len(x) != (offset_w+1), list_w_for_char)
        new_offset_l = offset_l + 1
        if new_offset_l < len(l):
            new_list_search_w.append(
                (
                    offset_l + 1,
                    offset_w + 1,
                    list_w_not_ending,
                    nb_w_found
                )
            )
    list_search_w = new_list_search_w

#print >> sys.stderr, "list_results:", list_results

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

print max(list_results)