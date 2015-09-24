import sys
import math
import operator

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# liste des puissances des chevaux
list_puissances = []

n = int(raw_input())
for i in xrange(n):
    pi = int(raw_input())
    # on ajoute la puissance dans la liste
    list_puissances.append(pi)

# on trie la liste des puissances
list_puissances.sort()

# la liste est triee. 
# -> On peut calculer par paire de puissances successives les differences
#    et recuperer la difference minimale
#print min(map(lambda x: x[1]-x[0], zip(list_puissances, list_puissances[1:])))
print min(map(operator.__sub__, list_puissances[1:], list_puissances[:-1]))

