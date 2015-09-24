import sys
import math
from collections import defaultdict

def update_short_dist_to_EI(graph_links, graph_dist, EI, dist_to_EI=0):
    """
    Recurvise method to set the minimal distance from each node (in graph_links) to a passerelle EI
    """
    if graph_dist[EI] > dist_to_EI:
        graph_dist[EI] = dist_to_EI
        for N in graph_links[EI]:
            update_short_dist_to_EI(graph_links, graph_dist, N, dist_to_EI+1)

def add_link(graph, N1, N2):
    ''' '''
    graph[N1].append(N2)
    graph[N2].append(N1)
    
def remove_link(graph, N1, N2):
    ''' '''
    graph[N1].remove(N2)
    if graph[N1] == []:
        del graph[N1]
    graph[N2].remove(N1)
    if graph[N2] == []:
        del graph[N2]
    
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

graph_links = defaultdict(list)
graph_dist = {}

 # N: the total number of nodes in the level, including the gateways
 # L: the number of links
 # E: the number of exit gateways
N, L, E = [int(i) for i in raw_input().split()]
for i in xrange(L):
     # N1: N1 and N2 defines a link between these nodes
    N1, N2 = [int(j) for j in raw_input().split()]
    #
    add_link(graph_links, N1, N2)
    #
    graph_dist[N1] = N
    graph_dist[N2] = N
    
#print >> sys.stderr, "graph_links: ", graph_links
#print >> sys.stderr, "graph_dist: ", graph_dist

for i in xrange(E):
    EI = int(raw_input()) # the index of a gateway node
    #
    update_short_dist_to_EI(graph_links, graph_dist, EI)
    
# game loop
while 1:
    SI = int(raw_input()) # The index of the node on which the Skynet agent is positioned this turn

    # on cherche la distance minimale a la passerelle EI la plus proche par rapport a la position SI
    node_to_remove = min(((node, graph_dist[node]) for node in graph_links[SI]), key=lambda x: x[1])[0]
    remove_link(graph_links, SI, node_to_remove)
            
    # Write the action
    print str(SI) + " " + str(node_to_remove)

