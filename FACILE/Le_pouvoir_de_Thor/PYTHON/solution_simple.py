import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# ---
# Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.

 # light_x: the X position of the light of power
 # light_y: the Y position of the light of power
 # initial_tx: Thor's starting X position
 # initial_ty: Thor's starting Y position
light_x, light_y, initial_tx, initial_ty = [int(i) for i in raw_input().split()]

cur_tx, cur_ty = initial_tx, initial_ty 
inc_dir = {'W': -1, 'E': +1, '': 0, 'N': -1, 'S': +1 }

# game loop
while 1:
    remaining_turns = int(raw_input())

    dir_y = 'N' if cur_ty > light_y else 'S' if cur_ty < light_y else ''
    dir_x = 'W' if cur_tx > light_x else 'E' if cur_tx < light_x else ''
    #
    cur_tx += inc_dir[dir_x]
    cur_ty += inc_dir[dir_y]
    
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # A single line providing the move to be made: N NE E SE S SW W or NW
    #print "SE"
    print dir_y+dir_x

