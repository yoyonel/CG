import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

N = int(raw_input())
# pre-allocate lists task (used for sorting tasks)
list_tasks = [()] * N
for i in xrange(N):
    J, D = [int(j) for j in raw_input().split()]
    # compute the end day
    E = J + D
    # add tupple to the list tasks
    list_tasks[i] = (J, E)
    
# sort list tasks with J (begin 'day' tasks)
list_tasks = sorted(list_tasks, key=lambda task: task[0])   # sort by J

#
nb_tasks = 0
# init: fist task
# take (and remove) the first task
task = list_tasks.pop(0)
# set the last task
last_J, last_E = task
#
for task in list_tasks:
    # get the current task
    cur_J, cur_E = task

    # compare the current task with the last one
    # if the current task begin before the end of the last task
    if cur_J < last_E:
        # if the end of the current task finish before the last task
        if cur_E <= last_E:
            # -> the current task is smaller than the last
            # we switch the last and current tasks
            last_E = cur_E
            last_J = cur_J
    else:
        # else the last task is 'isolated'
        # -> the last task is a 'valid' computation for our problem
        nb_tasks += 1
        # we switch the last and current tasks
        last_E = cur_E
        last_J = cur_J
        
# The last task of the list is a valid computation for our problem
nb_tasks += 1

# print out the result
print nb_tasks

