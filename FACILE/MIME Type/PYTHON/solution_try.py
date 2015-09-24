import sys
import math
import os, time

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# key: (lower) extension
# value: association mime a l'extension
dict_mime = {}

n = int(raw_input()) # Number of elements which make up the association table.
q = int(raw_input()) # Number Q of file names to be analyzed.
for i in xrange(n):
     # ext: file extension
     # mt: MIME type.
    ext, mt = raw_input().split()
    # on associe l'extension (lower case) au mime
    dict_mime[ext.lower()] = mt

for i in xrange(q):
    fname = raw_input() # One file name per line.
    # on cherche l'indice du dernier point dans fname
    # si -1: '.' non trouve dans la chaine
    # sinon indice du dernier point
    ind_last_dot = fname.rfind('.')
    try:
        # si -1: alors 'UNKNOWN'
        # sinon on recpere l'extension et on cherche la correspondance MIME associee
        print 'UNKNOWN' if ind_last_dot == -1 else dict_mime[fname[ind_last_dot+1:].lower()]
    except KeyError:
        # si pas de correspondance -> 'UNKNOWN'
        print 'UNKNOWN'

