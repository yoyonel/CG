import sys
import math
import ast

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = raw_input()
# n = "[1,2,5,6,7,9,12,55,56,57,58,60,61,62,64,65,70]"

# print >> sys.stderr, "n: ", n, type(n)

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

# print >> sys.stderr, "l: ", l
# http://stackoverflow.com/questions/1894269/convert-string-representation-of-list-to-list-in-python
l = ast.literal_eval(n)
l.sort()

diff_l = [(i - j) for i, j in zip(l[1:], l[:-1])]

# print >> sys.stderr, "diff_l: ", diff_l

result = []

state = 0

for i, n in enumerate(l[:-1]):
    diff = diff_l[i]

    if state == 0:
        result.append(n)
        if diff == 1:
            state = 1
    elif state == 1:
        if diff != 1:
            result.append(n)
            state = 0
        else:
            result.append('-')
            state = 2
    else:
        if diff != 1:
            result.append(n)
            state = 0
        else:
            state = 2
result.append(l[-1])

# http://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
# http://www.tutorialspoint.com/python/string_replace.htm
print (','.join(str(e) for e in result)).replace(',-,', '-')
