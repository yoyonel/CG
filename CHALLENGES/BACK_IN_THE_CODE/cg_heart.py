import sys
import math
import numpy as np
import random


def isOnBoard(pos_x, pos_y):
    """

    :param pos_x:
    :param pos_y:
    :return:
    """
    return 0 <= pos_x < 35 and 0 <= pos_y < 20


nb_samples = 15

# HEART FUNCTION
t = np.linspace(-math.pi, math.pi, nb_samples)
func_heart_x = 3.9*np.sin(t)**3
func_heart_y = 3*np.cos(t)-1.2*np.cos(2*t)-0.6*np.cos(3*t)-0.2*np.cos(4*t)
max_func_heart_x = max(func_heart_x)
min_func_heart_x = min(func_heart_x)
max_func_heart_y = max(func_heart_y)
min_func_heart_y = min(func_heart_y)
#
func_heart_x -= min_func_heart_x
func_heart_x /= (max_func_heart_x - min_func_heart_x)
func_heart_y -= min_func_heart_y
func_heart_y /= (max_func_heart_y - min_func_heart_y)
func_heart_y *= max_func_heart_y/max_func_heart_x
#
func_heart_x *= 3
func_heart_y *= 3

#import matplotlib.pyplot as plt
#plt.plot(x, y); plt.show()

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

opponent_count = int(raw_input())  # Opponent count

i_heart = 0
dst_x = 0
dst_y = 0
bFirst = True

# game loop
while 1:
    game_round = int(raw_input())
    # x: Your x position
    # y: Your y position
    # back_in_time_left: Remaining back in time
    x, y, back_in_time_left = [int(i) for i in raw_input().split()]
    for i in xrange(opponent_count):
        # opponent_x: X position of the opponent
        # opponent_y: Y position of the opponent
        # opponent_back_in_time_left: Remaining back in time of the opponent
        opponent_x, opponent_y, opponent_back_in_time_left = [int(j) for j in raw_input().split()]
    board = []
    for i in xrange(20):
        line = raw_input()  # One line of the map ('.' = free, '0' = you, otherwise the id of the opponent)
        board.append(line)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # action: "x y" to move or "BACK rounds" to go back in time
    #print "17 10"
    if bFirst:
        dst_x, dst_y = x, y
        bFirst = False

    if (x == dst_x) & (y == dst_y):
        dx = func_heart_x[i_heart]
        dy = func_heart_y[i_heart]
        nb_try = 0
        while ((not isOnBoard(x+dx, y+dy)) | (board[y][x] != '.')) & i_heart:
            i_heart = (i_heart+1) % nb_samples
            if not i_heart:
                x = int(random.random()*35)
                y = int(random.random()*20)
            dx = func_heart_x[i_heart]
            dy = func_heart_y[i_heart]
            nb_try += 1
        #print >> sys.stderr, "New dest: ", dst_x, dst_y
        dst_x, dst_y = int(x+dx), int(y+dy)
        i_heart = (i_heart+1) % nb_samples
        if (not i_heart) | (nb_try > 5):
                x = int(random.random()*35)
                y = int(random.random()*20)

    print dst_x, ' ', dst_y