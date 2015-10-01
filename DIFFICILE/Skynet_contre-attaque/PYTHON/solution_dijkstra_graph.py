import sys
import math

# url: http://www.redblobgames.com/pathfinding/a-star/implementation.html#optimizations
class Graph(object):
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]

    def add_edge(self, N1, N2):
        self.edges.setdefault(N1, []).append(N2)
        self.edges.setdefault(N2, []).append(N1)

    def del_edge(self, a, b):
        self.edges[N1].remove(N2)
        self.edges[N2].remove(N1)


class GraphWithWeights(Graph):
    def __init__(self):
        self.weights = {}
        #
        super(GraphWithWeights, self).__init__()

    def cost(self, a, b):
        # cout de base de deplacement egale a un tour de jeu (par defaut)
        return self.weights.get(b, 1)


class GraphForSkyNetProblem(GraphWithWeights):
    def __init__(self):
        self.connectivities = {}
        self.list_nodes_c2 = []
        self.list_EI = []
        #
        super(GraphForSkyNetProblem, self).__init__()

    def update(self, list_EI):
        """ 
            Mise a jour des informations:
            - le cout de deplacement vers un noeud
            - la connectivite d'un noeud vers les passerelles (combien de passerelles sont accessibles pour un noeud)
        """
        #
        self.list_EI = list_EI
        # on parcourt la liste des noeuds passerelles
        for a in list_EI:
            # pour tout les voisins des noeuds passerelles
            for b in self.edges[a]:
                # on assigne un cout de passage a 0
                # car quand skynet est a 1 de distance d'un noeud passerelle
                # le tour de jeu est force pour empecher skynet d'atteindre la passerelle a proximite
                # donc le cout de deplacement pour skynet est au final ~ nul
                self.weights[b] = 0

                # on met a jour la valeur de connectivite a des passerelles
                self.add_connectivity(b)
                if self.connectivity(b) == 2:
                    self.list_nodes_c2.append(b)

    def connectivity(self, a):
        """ connectivite vers des passerelles """
        # par defaut un noeud n'est pas relie a une passerelle
        return self.connectivities.get(a, 0)

    def add_connectivity(self, a):
        """ Ajoute une connectivite aux passerelles au noeud a """
        self.connectivities[a] = self.connectivity(a) + 1

    def del_connectivity(self, a):
        """ Ajoute une connectivite aux passerelles au noeud a """
        self.connectivities[a] = self.connectivity(a) - 1

    def get_nearest_node_c2(self, SI):
        """ 
            Calcul et renvoie le node de connectivite 2 (si present) par rapport a une position SI de skynet
        """
        # par defaut on ne trouve pas de node c2
        nearest_node_c2 = -1
        #
        if self.list_nodes_c2:
            dict_nodes_c2 = {}
            # parcourt de la liste des nodes de connectivites 
            for a in self.list_nodes_c2:
                # on calcul le "short" path vers ce noeud C2
                came_from, cost_so_far = dijkstra_search(self, SI, a)
                # reconstructed the path and the cost associated
                path, cost = reconstruct_path_cost(came_from, cost_so_far, start=SI, goal=a)
                # on conserve le cout du chemin pour aller au node c2
                dict_nodes_c2[a] = cost
            # on recupere le node C2 le moins couteux (<=> le plus rapidement accessible par skynet)
            nearest_node_c2 = min(dict_nodes_c2.items(), key=lambda x: x[1])[0]
        #
        return nearest_node_c2

    def get_gateways(self, a):
        """ Renvoie la liste des passerelles dans le voisinage du node a """
        # on effectue une intersection entre les listes:
        # - des noeuds du voisinages de a
        # - la liste des passerelles
        return set(self.edges[a]).intersection(self.list_EI)

    def del_node_c2(self, a):
        """ On retire un node a C2 du graphe """
        # on retire le noeud a de la liste des nodes C2
        self.list_nodes_c2.remove(a)

    def del_link_to_gateway(self, a, EI):
        """ On retire le lien d'un node a vers une passerelle EI """
        # on reduit la connectivite du node a
        self.del_connectivity(a)
        # on retire le lien dans le graph
        self.del_edge(a, EI)
        # on verifie que la passerelle EI est toujours accessible
        if not self.edges[EI]:
            # si non accessible, on la retire de la liste des EI
            self.list_EI.remove(EI)


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
        # print >> sys.stderr, "current: ", current
        current = came_from[current]
        path.append(current)
        cost += cost_so_far[current]
    path.reverse()
    return (path, cost)


graph_network = GraphForSkyNetProblem()

# N: the total number of nodes in the level, including the gateways
# L: the number of links
# E: the number of exit gateways
N, L, E = [int(i) for i in raw_input().split()]
for i in xrange(L):
    # N1: N1 and N2 defines a link between these nodes
    N1, N2 = [int(j) for j in raw_input().split()]
    #
    graph_network.add_edge(N1, N2)

list_EI = []
for i in xrange(E):
    EI = int(raw_input())  # the index of a gateway node
    #
    list_EI.append(EI)

graph_network.update(list_EI)

# print >> sys.stderr, "graph_network.edges: ", graph_network.edges
#print >> sys.stderr, "graph_network.weights: ", graph_network.weights
#print >> sys.stderr, "graph_network.connectivities: ", graph_network.connectivities

# link (N1, N2) to remove
N1 = N2 = 0

b_still_nodes_c2 = True

# game loop
while 1:
    SI = int(raw_input())  # The index of the node on which the Skynet agent is positioned this turn

    # a t'on des passerelles dans le voisinage de la postion SI de skynet ?
    list_EI_close_to_SI = graph_network.get_gateways(SI)
    if list_EI_close_to_SI:
        # si oui (normalement une seule passerelle proche)
        EI = list_EI_close_to_SI.pop()
        #
        N1 = SI
        N2 = EI
    else:
        if b_still_nodes_c2:
            # on recupere le node C2 le plus proche de la position SI de skynet
            node_c2 = graph_network.get_nearest_node_c2(SI)
            # si il n'y a pas plus de noeud c2
            if node_c2 == -1:
                # on met a jour la variable booleenne
                b_still_nodes_c2 = False
            else:
                # sinon on retire un lien entre le node c2 et une passerelle a laquelle il est connecte
                N1 = node_c2
                # on recupere une passerelle de la liste des passerelles accessibles pour le node C2
                # ps: il n'y a pas de strategie d'optimisation du choix de la passerelle ici ! (a optimiser/ameliorer)
                N2 = graph_network.get_gateways(node_c2).pop()
                #
                graph_network.del_node_c2(node_c2)
        #        
        if not b_still_nodes_c2:
            # on prend n'importe quelle passerelle, et n'importe quel noeud au voisinage de la passerelle
            # on retire ce lien
            # ps: il n'y a pas de strategie d'optimisation dans les choix de passerelles, noeuds au voisiginage de la
            # passerelle ici ! (a optimiser/ameliorer si on veut minimiser le nombre de coup a jouer)
            # on recupere la premiere passerelle de la liste
            EI = graph_network.list_EI[0]
            # on recupere le premier node voisin de la passerelle EI
            NE_EI = graph_network.edges[EI][0]
            #
            N1 = NE_EI
            N2 = EI

    # on retire l'edge (le lien) dans le graphe
    # N1: node
    # N2: node passerelle
    graph_network.del_link_to_gateway(N1, N2)

    # print out the result : link to remove
    print str(N1) + " " + str(N2)
