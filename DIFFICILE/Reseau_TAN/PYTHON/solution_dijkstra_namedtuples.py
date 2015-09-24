import sys
import math

import math
from collections import namedtuple
from collections import defaultdict

# grosse inspiration (voir copier-coller massif) de 'Skynet contre-attaque'
NT_Station = namedtuple(
    'Stop',
    [
        'id',
        'full_name',
        'description',
        'lat',
        'long',
        'zone',
        'url',
        'type',
        'parent'
    ]
)
        
class Station(NT_Station):
    def __init__(self, str_Station, prefix_Station='StopArea:'):
        super(Station, self).__init__()

    def __new__(_cls, str_Station, prefix_Station='StopArea:'):
        'Create a new instance of '
        new_inst = None
        #url: http://www.tutorialspoint.com/python/string_startswith.ht
        if str_Station.startswith(prefix_Station):
            #str_Station = str_Station[len(prefix_Station):]
            split_str_Station = str_Station.split(',')
            split_str_Station = Station.convert_split(split_str_Station)
            new_inst = NT_Station.__new__(_cls, *split_str_Station)
        return new_inst
    
    @staticmethod
    def convert_Station(str_Station, prefix_Station='StopArea:'):
        ''
        return str_Station[len(prefix_Station):]
        
    @staticmethod
    def convert_split(split_str_Station):
        ''
        split_str_Station[0] = Station.convert_Station(split_str_Station[0])
        split_str_Station[1] = split_str_Station[1][1:-1]
        split_str_Station[3] = math.radians(float(split_str_Station[3]))
        split_str_Station[4] = math.radians(float(split_str_Station[4]))
        return split_str_Station

    def distance(self, dst):
        ''' '''
        x = (dst.long - self.long)*math.cos((self.lat + dst.lat)*0.5)
        y = dst.lat - self.lat
        d = math.sqrt(x**2 + y**2) * 6371
        #d = math.sqrt(x**2 + y**2)     # on peut ne pas normaliser la distance
        return d
        
# url: http://www.redblobgames.com/pathfinding/a-star/implementation.html#optimizations
class Graph(object):
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        ''' '''
        return self.edges[id]
        
    def add_edge(self, N1, N2):
        ''' '''
        self.edges.setdefault(N1, []).append(N2)
        
    def del_edge(self, a, b):
        ''' '''
        self.edges[N1].remove(N2)

class GraphWithWeights(Graph):
    def __init__(self):
        ''' '''
        self.weights = defaultdict(dict)
        super(GraphWithWeights, self).__init__()
        
    def cost(self, a, b):
        #
        return self.weights[a][b]
        

class GraphForTAN(GraphWithWeights):
    def __init__(self, dict_stations):
        ''' '''
        self.dict_stations = dict_stations
        super(GraphForTAN, self).__init__()
        
    def compute_costs(self):
        ''' '''
        for start, stops in self.edges.iteritems():
            for stop in stops:
                self.weights[start][stop] = self.dict_stations[start].distance(self.dict_stations[stop])

import collections
import heapq

class PriorityQueue:
    """ Wrapper sur heapq (utilisation simplifiee) """
    
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
    
def reconstruct_path_cost(came_from, cost_so_far, start, goal):
    current = goal
    path = [current]
    cost = cost_so_far[current]
    while current != start:
        #print >> sys.stderr, "current: ", current
        current = came_from[current]
        path.append(current)
        cost += cost_so_far[current]
    path.reverse()
    return (path, cost)
    
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

start_point = raw_input()
end_point = raw_input()

start_point = Station.convert_Station(start_point)
end_point = Station.convert_Station(end_point)

n = int(raw_input())
dict_stations = {}
for i in xrange(n):
    stop = raw_input()
    #
    obj_Station = Station(stop)   # construct object 'Stop' from string description
    dict_stations[obj_Station.id] = obj_Station  # store 'stop' object with the id
#for id_Station, obj_Station in dict_stations.iteritems():
#    print >> sys.stderr, "%s = %s" % (id_Station, obj_Station)

m = int(raw_input())
#url: https://www.accelebrate.com/blog/using-defaultdict-python/
graph_routes = GraphForTAN(dict_stations)  # on transmet le dict des stops pour le calcul des poids/distances sur les stops
for i in xrange(m):
    route = raw_input()
    #
    start, stop = map(Station.convert_Station, route.split(' '))  # on converti les strings en id de stations
    #
    graph_routes.add_edge(start, stop)

graph_routes.compute_costs()
#print >> sys.stderr, "graph_routes.weights: %s" % graph_routes.weights

# 
came_from, cost_so_far = dijkstra_search(graph_routes, start_point, end_point)
try:
    # reconstructed the path and the cost associated
    path = reconstruct_path(came_from, start=start_point, goal=end_point)
    #print >> sys.stderr, "path, cost: %s, %s" % (path, cost)
    
    for id_Station in path:
        print dict_stations[id_Station].full_name
except:
    print 'IMPOSSIBLE'
