#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# import sys
# import math
import numpy as np
import textwrap

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height = [int(i) for i in raw_input().split()]

# utilisation d'un np array pour l'outil d'addtion de vecteurs (list de int)
nb_sharps_in_columns = np.zeros(width)

for i in xrange(height):
    line = raw_input()
    nb_sharps_in_columns = np.add(
        [c == '#' for c in line],   # auto cast vers np.array
        nb_sharps_in_columns
    )

result = ''.join(
    [
        '#' if (height - i) <= nb_sharps_in_columns[j]
        else '.'
        for i, j in np.ndindex((height, width))
    ]
)

# url: http://stackoverflow.com/questions/2657693/insert-a-newline-character-every-64-characters-using-python
# => tous les 'width' caractères, on rajoute un 'saut de ligne'
result = '\n'.join(textwrap.wrap(result, width))

print result
