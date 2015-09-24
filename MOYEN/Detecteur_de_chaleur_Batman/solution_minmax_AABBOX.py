import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

 # w: width of the building.
 # h: height of the building.
w, h = [int(i) for i in raw_input().split()]
n = int(raw_input()) # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]

min_x, max_x, min_y, max_y = 0, w, 0, h

# game loop
while 1:
    bomb_dir = raw_input() # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)

    min_x = min_x if bomb_dir.find("R")==-1 else x0
    max_x = max_x if bomb_dir.find("L")==-1 else x0
    min_y = min_y if bomb_dir.find("D")==-1 else y0
    max_y = max_y if bomb_dir.find("U")==-1 else y0
    
    x0, y0 = (max_x+min_x)*0.5, (max_y+min_y)*0.5
    
    print "%d %d" % (x0, y0)
