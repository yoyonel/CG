import sys
import math
from itertools import chain

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input()) # the number of adjacency relations

# dictionnary: dict_graph_parents
# - key: id du parent de la connection
# - value: liste des enfants connectes a ce parent
dict_graph_parents = {}
# dictionnary: dict_graph_parents
# - key: id de l'enfant de la connection
# - value: liste des parents connectes a cet enfant
dict_graph_childs = {}
# liste des id des enfants
set_childs = set()
for i in xrange(n):
     # xi: the ID of a person which is adjacent to yi
     # yi: the ID of a person which is adjacent to xi
    xi, yi = [int(j) for j in raw_input().split()]
    
    # update dictionnaries
    dict_graph_parents.setdefault(xi, []).append(yi)
    dict_graph_childs.setdefault(yi, []).append(xi)
    
    # on met a jour la liste des enfants
    set_childs.add(yi)
    
#print >> sys.stderr, "dict_graph_parents: ", dict_graph_parents
#print >> sys.stderr, ""

length_of_influence = 1

# on boucle tant qu'il y a des parents dans le graphe
while(dict_graph_parents):
    # on construit le set des id des nodes (encore) actifs
    # c'est l'union entre les parents et les enfants connectes
    set_parents = set(dict_graph_parents.keys())
    set_nodes = set_parents
    set_nodes.update(set_childs)
    #print >> sys.stderr, "set_nodes:", set_nodes
    
    # on peut determiner alors les enfants par rapport au graph (node sans lien vers un autre enfant)
    set_childs_only = set_nodes.difference(set(dict_graph_parents.keys()))
    #print >> sys.stderr, "set_childs_only:", set_childs_only
    
    # on parcourt la liste des enfants detectes qu'on retire du graphe
    for child in set_childs_only:
        # pour chaque parent connecte a cet enfant
        for parent in dict_graph_childs[child]:
            # on retire la connection
            dict_graph_parents[parent].remove(child)
        set_childs.remove(child)
    # on a modifie le graph parent, on verifie qu'on a pas cree des nodes parents sans enfants
    dict_graph_parents = {k: v for k, v in dict_graph_parents.iteritems() if v}
    #print >> sys.stderr, "dict_graph_parents: ", dict_graph_parents
    
    # on a etabli un niveau d'influence supplementaire parent->enfant
    length_of_influence += 1

print length_of_influence
