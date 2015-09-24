import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

road = int(raw_input()) # the length of the road before the gap.
gap = int(raw_input()) # the length of the gap.
platform = int(raw_input()) # the length of the landing platform.

# To debug: print >> sys.stderr, "Debug messages..."
#print >> sys.stderr, "road: ", road
#print >> sys.stderr, "gap: ", gap
#print >> sys.stderr, "platform: ", platform

b_passed_the_gap = False

# game loop
while 1:
    speed = int(raw_input()) # the motorbike's speed.
    coord_x = int(raw_input()) # the position on the road of the motorbike.

    if b_passed_the_gap:
        print "SLOW"
    else:
        if speed <= gap:
            print "SPEED"
        elif speed > gap+1:
            print "SLOW"
        elif coord_x + speed < road:
            print "WAIT"
        else:
            print "JUMP"
            b_passed_the_gap = True

