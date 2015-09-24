import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

x = []
y = []
N = int(raw_input())
for i in xrange(N):
    num, t = [int(j) for j in raw_input().split()]
    #
    x.append(num)
    y.append(t)
# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

max_x, min_x = max(x), min(x)
max_y, min_y = max(y), min(y)
print >> sys.stderr, "min_x, max_x: ", min_x, max_x
print >> sys.stderr, "min_y, max_y: ", min_y, max_y
print >> sys.stderr, "x: ", x[0:10]

delta_min_max_x = float(max_x - min_x)
delta_min_max_y = float(max_y - min_y)

x = map(lambda x: (float(x) - min_x)/delta_min_max_x*10 + 1, x)

y = map(lambda x: (float(x) - (min_y-1))/delta_min_max_y, y)

max_x, min_x = max(x), min(x)
max_y, min_y = max(y), min(y)
print >> sys.stderr, "min_x, max_x: ", min_x, max_x
print >> sys.stderr, "min_y, max_y: ", min_y, max_y
print >> sys.stderr, "x: ", x[0:10]

# for: 2**n
#y = map(lambda value : math.log(value)/math.log(2.0), y)
# for: n**3
#y = map(lambda value : math.pow(value, 1.0/3.0), y)
# for: n**2
#y = map(lambda value : math.pow(value, 1.0/2.0), y)

#
x = np.asarray(x)
y = np.asarray(y)
#
A = np.vstack((x, np.ones(N))).T
model, resid = np.linalg.lstsq(A, y)[:2]

r2 = 1 - resid / (y.size * y.var())
print >> sys.stderr, "r2: ", r2

print "answer"

dx = np.gradient(x)
dy = np.gradient(y, dx)

print 'dx: ', dx[0:20]
print 'dy: ', dy[0:20]

import matplotlib.pyplot as plt
# _ = plt.plot(x, 
# 	y, 'ko',
# 	 #np.exp(y), 'r-'
# 	 )
_ = plt.plot(
	x,
	np.power(dy, -1)
	)

plt.show()
