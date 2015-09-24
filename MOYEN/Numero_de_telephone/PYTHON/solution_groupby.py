import sys
import math
import itertools

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
list_telephones = []
for i in xrange(n):
    telephone = raw_input()
    #
    list_telephones.append(telephone)

# on trie la liste des numeros de telephones    
list_telephones.sort()

list_groups_telephones = [list_telephones]
nb_elems = 0
i = 0
# tant qu'il reste des telephones (ou groupes de numeros de tels) a traiter
while(list_groups_telephones):
    next_list_groups_telephones = []
    # pour chaque groupe de tels
    for list_telephones in list_groups_telephones:
        # on groupby sur le digit i-eme digit
        for key, igroup in itertools.groupby(list_telephones, lambda x: x[i]):
            lgroup = list(igroup)
            # si le nombre de tel dans ce groupby est superieur a 1
            # => plusieurs telephones avec cette racine de digit
            if len(lgroup) > 1:
                # on supprime les telephones qui ne possedent plus de digits (exactement inclus)
                next_lgroup = filter(lambda x: len(x) > i+1, lgroup)
                # on rajoute le groupe des tels restant pour la prochaine iteration
                next_list_groups_telephones.append(next_lgroup)
                # on rajoute ce prefixe au nombre d'elements
                nb_elems += 1
            else:
                # sinon un seul numero avec cette racine
                # on rajoute la longueur du prefixe au nombre d'elements
                nb_elems += len(lgroup[0][i:])
    # on itere le processus sur les tels restant
    list_groups_telephones = next_list_groups_telephones
    # prochaine iteration
    i += 1

# The number of elements (referencing a number) stored in the structure.
print nb_elems

