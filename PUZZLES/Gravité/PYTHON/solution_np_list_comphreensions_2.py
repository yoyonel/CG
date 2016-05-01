#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# import sys
# import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height = [int(i) for i in raw_input().split()]

# utilisation d'un np array pour l'outil d'addtion de vecteurs (list de int)
nb_sharps_in_columns = reduce(
    lambda a, b: np.add(a, b),
    [
        map(lambda c: c == '#', raw_input())
        for _ in xrange(height)
    ],
    np.zeros(width)
)

# urls:
# http://stackoverflow.com/questions/4937491/matrix-transpose-in-python
# -> http://stackoverflow.com/a/4937526
# https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions
# https://docs.python.org/3/tutorial/controlflow.html#tut-unpacking-arguments
# utilisation de zip(*) pour transposer les données
result = ''.join(
    reduce(
        lambda a, b: a + tuple('\n') + b,
        zip(*[
            '.' * (height - nb_sharp_in_one_column) + '#' * nb_sharp_in_one_column
            for nb_sharp_in_one_column in nb_sharps_in_columns
        ]
        )
    )
)

print result
