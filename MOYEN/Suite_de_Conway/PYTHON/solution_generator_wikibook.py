import sys
import math
import itertools

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

r = int(raw_input())
l = int(raw_input())

# inspire de ->
# url: https://fr.wikibooks.org/wiki/Suite_de_Conway#En_Python
def conway(begin=1):
    x = [begin]
    while True:
        yield x
        nx = []
        for item, grouper in itertools.groupby(x):
            nx.extend([len(list(grouper)), item])
        x = nx

suite = conway(r)
# url: https://docs.python.org/2/library/functions.html#next
'''
for _ in range(l-1):
    print >> sys.stderr, suite.next()
'''
[suite.next() for _ in xrange(l-1)]

answer = ' '.join(str(x) for x in suite.next())

print answer
