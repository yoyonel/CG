import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

dict_graph = {}

n = int(raw_input()) # the number of adjacency relations
for i in xrange(n):
     # xi: the ID of a person which is adjacent to yi
     # yi: the ID of a person which is adjacent to xi
    xi, yi = [int(j) for j in raw_input().split()]
    
    # build a non oriented graph
    dict_graph.setdefault(xi, set()).add(yi)
    dict_graph.setdefault(yi, set()).add(xi)

#print >> sys.stderr, "dict_graph: ", dict_graph
#print >> sys.stderr, ""

height_graph = 0
# loop until element (node) exist in graph
while dict_graph:
    # get the 'isolated' nodes 
    # -> list comphreension
    list_isolated_nodes = [node for node, neighboors in dict_graph.iteritems() if len(neighboors) == 1]
    # for each isolated node
    for isolated_node in list_isolated_nodes:
        for neighboor in dict_graph[isolated_node]:
            dict_graph[neighboor].remove(isolated_node)
        # remove the isolated node
        del dict_graph[isolated_node]
    # remove empty (= []) node in dict
    # url: http://stackoverflow.com/questions/2844516/python-filter-a-dictionary
    # -> dict comphreension
    dict_graph = {k: v for k, v in dict_graph.iteritems() if v}
    #
    height_graph += 1
    
print height_graph
