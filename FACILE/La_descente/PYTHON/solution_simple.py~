import sys, math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
while 1:
    SX, SY = [int(i) for i in raw_input().split()]
    list_MH = [0]*8
    for i in xrange(8):
        MH = int(raw_input()) # represents the height of one mountain, from 9 to 0. Mountain heights are provided from left to right.
        list_MH[i] = MH
    
    id_max_height = list_MH.index(max(list_MH))
    print >> sys.stderr, "id_max_height: ", id_max_height
    
    if SX == id_max_height:
        print "FIRE"
    else:
        print "HOLD"
        
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    
    #print "HOLD" # either:  FIRE (ship is firing its phase cannons) or HOLD (ship is not firing).
