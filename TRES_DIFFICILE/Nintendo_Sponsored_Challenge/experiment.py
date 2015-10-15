__author__ = 'latty'

from collections import defaultdict

size = 32
dict_indices_i_j = defaultdict(list)
dict_iter_for_b = defaultdict(int)
for i in range(size):
    for j in range(size):
        indice_for_b = (i + j) / 32
        dict_indices_i_j[indice_for_b].append((i, j))
        #
        indice_bit_for_b = (i + j) % 32
        indice_bit_for_a0 = i % 32
        indice_bit_for_a1 = j % 32
        #
        dict_iter_for_b[indice_bit_for_b] += 1
        indice_iter_for_b = dict_iter_for_b[indice_bit_for_b]
        # if (indice_for_b == 0) & (indice_iter_for_b == 2) & (indice_bit_for_b == 10):
        if (indice_for_b == 0) & (indice_bit_for_b == 1):
            #if indice_bit_for_a0 == 1:
            #
            print 'b%d(iter:%d, bit:%d) = b%d(iter:%d, bit:%d) ^ (a0(bit:%d) & a1(bit:%d))' % (
                #
                indice_for_b,
                indice_iter_for_b,
                indice_bit_for_b,
                #
                indice_for_b,
                indice_iter_for_b - 1,
                indice_bit_for_b,
                #
                indice_bit_for_a0,
                indice_bit_for_a1
            )
'''
print "for dict_indices_i_j[0]:"
print [(i, j) for i, j in dict_indices_i_j[0] if ((i + j) % 32) is 0]
print [(i, j) for i, j in dict_indices_i_j[0] if ((i + j) % 32) is 1]
print [(i, j) for i, j in dict_indices_i_j[0] if ((i + j) % 32) is 2]

print "for dict_indices_i_j[1]:"
print [(i, j) for i, j in dict_indices_i_j[1] if ((i + j) % 32) is 30]
print [(i, j) for i, j in dict_indices_i_j[1] if ((i + j) % 32) is 29]
print [(i, j) for i, j in dict_indices_i_j[1] if ((i + j) % 32) is 28]
'''