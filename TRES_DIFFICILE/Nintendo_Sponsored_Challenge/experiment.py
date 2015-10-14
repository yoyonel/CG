__author__ = 'latty'

from collections import defaultdict

size = 32
dict_indices_i_j = defaultdict(list)
for i in range(size):
    for j in range(size):
        indice = (i + j) / 32
        dict_indices_i_j[indice].append((i, j))

print "for dict_indices_i_j[0]:"
print [(i, j) for i, j in dict_indices_i_j[0] if ((i + j) % 32) is 0]
print [(i, j) for i, j in dict_indices_i_j[0] if ((i + j) % 32) is 1]
print [(i, j) for i, j in dict_indices_i_j[0] if ((i + j) % 32) is 2]

print "for dict_indices_i_j[1]:"
print [(i, j) for i, j in dict_indices_i_j[1] if ((i + j) % 32) is 30]
print [(i, j) for i, j in dict_indices_i_j[1] if ((i + j) % 32) is 29]
print [(i, j) for i, j in dict_indices_i_j[1] if ((i + j) % 32) is 28]