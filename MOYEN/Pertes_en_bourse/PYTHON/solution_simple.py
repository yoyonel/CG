import sys
import math
#
import operator

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
vs = raw_input()

# convert string to list int (separator ' ')
vs_int = [int(i) for i in vs.split()]
#print >> sys.stderr, "vs_int = ", vs_int    

perte_maximale = 0
min_value = max_value = 0
# traitement iteratif => O(n)
for i in vs_int:
    # est ce que la valeur courante est superieure a notre max_value actuelle ?
    if max_value < i:
        # si oui, on met a jour le max courant
        max_value = i
        # on reset la recherche du plus grand ecart (~ perte)
        min_value = max_value
    # ou est ce que la valeur courante est inferieure  anotre min_value actuelle ?
    elif min_value > i:
        # si oui, on met a jour la perte_maximale
        # on prend en compte le nouveau differentiel (perte) courante
        perte_maximale = min(perte_maximale, i - max_value)
        # on met a jour notre min_value
        min_value = i
    #
    # DEBUG
    #
    #print >> sys.stderr, "i = ", i
    #print >> sys.stderr, "max_value = ", max_value
    #print >> sys.stderr, "min_value = ", min_value
    #print >> sys.stderr, "perte_courante = ", perte_courante
    #print >> sys.stderr, "perte_maximale = ", perte_maximale
    #print >> sys.stderr, ""

# pour etre conforme aux contraintes de sortie des resultats
perte_maximale = 0 if perte_maximale > 0 else perte_maximale

# print out the result
print perte_maximale

