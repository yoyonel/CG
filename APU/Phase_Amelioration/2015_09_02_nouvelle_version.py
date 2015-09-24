import sys
import math
from itertools import chain
from operator import itemgetter

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
            
class Node:
    """
    """
    # ENUM
    E_Dir = Enum(['UP', 'DOWN', 'LEFT', 'RIGHT'])

    def __init__(self, x, y, nb_link):
        """
        """        
        # Position : x, y
        self.x = x
        self.y = y

        # Amount: init, current
        self.nb_link_init = int(nb_link)
        self.nb_link_cur = self.nb_link_init

        # Voisinage
        # Valency : combien de voisins (accessibles) autour du node
        self.valency = 0
        # id des nodes voisins (selon les directions)        
        self.dict_neighboors = dict.fromkeys(Node.E_Dir, -1)

    def __repr__(self):
        """
        """
        return self.__str__()
        
    def __str__(self):
        """
        """
        return "(%d, %d) - (%d, %d) - Neighboors: %s -> Valency:%d" % (self.x, self.y, self.nb_link_init, self.nb_link_cur, self.dict_neighboors, self.valency)
        
    def set_neighboor(self, dir, id):
        """
        """
        self.dict_neighboors[dir] = id
        
    def get_neighboor(self, dir):
        """
        """
        return self.dict_neighboors[dir]
        
    def update_valency(self):
        """
        """
        self.valency = 4 - self.dict_neighboors.values().count(-1)
        return self.valency            

    def decrement_valency(self):
        """
        """        
        self.valency -= 1
        
    def get_amount(self):
        """
        """
        return self.nb_link_cur

    def reduce_amount(self, amount):
        """
        """
        self.nb_link_cur -= amount

    def is_valid(self):
        """
        """
        return self.nb_link_cur > 0

class Link:
    """
    """

    E_TypeLink = Enum(['HORIZONTAL', 'VERTICAL'])    

    def __init__(self, node_0, node_1, amount):
        """
        """
        
        
        self._node_0 = node_0
        self._node_1 = node_1
        
        self._amount = amount

        if node_0.x == node_1.x:
            # type link is vertical
            self._type_link = Link.E_TypeLink.VERTICAL
            #
            self._offset = node_0.x
            #
            self._min = min(node_0.y, node_1.y)
            self._max = max(node_0.y, node_1.y)
        else:
            # type link is vertical
            self._type_link = Link.E_TypeLink.HORIZONTAL
            #
            self._offset = node_0.y
            #
            self._min = min(node_0.x, node_1.x)
            self._max = max(node_0.x, node_1.x)

    @staticmethod
    def compute_type(node_0, node_1):
        """
        """
        return Link.E_TypeLink.VERTICAL if node_0.x == node_1.x else Link.E_TypeLink.HORIZONTAL
        
    def get_axis(self):
        """
        """
        return self._type_link
        
    def intersect(self, link):
        """
        """
        return  (self._type_link != link._type_link) & \
                (link._min < self._offset < link._max) & \
                (self._min < link._offset < self._max)
        
    def __str__(self):
        return "nodes: %d <-> %d, amount: %d, type: %s" % (self._node_0, self._node_1, self.amount, self._type_link)
        
        
class Network:
    """
    """
    def __init__(self, width, height):
        """
        """
        # dimension de la grille 
        self.width = width
        self.height = height
        #
        self.s_grid = [['.' for i in range(width)] for j in range(height)]
        #
        self.hv_grid = {Link.E_TypeLink.VERTICAL: {}, Link.E_TypeLink.HORIZONTAL: {}}
        #self.hv_grid = dict.fromkeys(Link.E_TypeLink, dict())   # FAILED: je comprend pas pourquoi !
        #
        self.list_nodes = []
        #
        self.list_ids_active_nodes = []
        self.list_ids_removed_nodes = []
        #
        self.dict_links = dict.fromkeys(Link.E_TypeLink, [])
        #
        self.__dict_dir_from_axis = { 
            Link.E_TypeLink.VERTICAL: (Node.E_Dir.UP, Node.E_Dir.DOWN),
            Link.E_TypeLink.HORIZONTAL: (Node.E_Dir.LEFT, Node.E_Dir.RIGHT)
        }
        #
        self.__dict_inv_dir = dict(
            chain.from_iterable(
                [
                    ((dir_neg, dir_pos), (dir_pos, dir_neg)) 
                    for dir_neg, dir_pos in self.__dict_dir_from_axis.values()
                ]
            )
        )
        #
        self.__dict_axis_from_dir = dict(
            chain.from_iterable(
                [
                    [(dir, axis) for dir in list_dir] 
                    for (axis, list_dir) in self.__dict_dir_from_axis.iteritems()
                ]
            )
        )
    
    def add_line(self, y, line):
        """
        """
        self.s_grid[y] = line
        
    def build(self):
        """
        """
        id_node = 0
        y = 0
        for line in self.s_grid:
            print >> sys.stderr, "line: ", line
            x = 0
            for nb_link in line:
                if nb_link != '.':
                    node = Node(x, y, nb_link)
                    #
                    self.list_nodes.append(Node(x, y, nb_link))
                    self.list_ids_active_nodes.append(id_node)
                    #
                    self.hv_grid['VERTICAL'].setdefault(x, {}).setdefault(y, id_node)
                    self.hv_grid['HORIZONTAL'].setdefault(y, {}).setdefault(x, id_node)
                    #
                    id_node += 1
                x += 1
            y += 1
            
        self.__build_axis_neighboors('VERTICAL')
        self.__build_axis_neighboors('HORIZONTAL')
        
        self._update_valencies()

    def __build_axis_neighboors(self, axis_name):
        """
        """
        attr_name_pos, attr_name_neg = self.__dict_dir_from_axis[axis_name]
        
        for axis in self.hv_grid[axis_name].iteritems():
            id_nodes_on_axis = sorted(axis[1].values())
            
            print >> sys.stderr, "nodes_on_%s: %s" % (axis_name, id_nodes_on_axis)

            #url: http://stackoverflow.com/questions/4029436/subtracting-the-current-and-previous-item-in-a-list
            for id_node_axis_pos, id_node_axis_neg in [(id_node_axis_neg, id_node_axis_pos) for id_node_axis_neg, id_node_axis_pos in zip(id_nodes_on_axis, id_nodes_on_axis[1:])]:
                #
                node_axis_pos = self.list_nodes[id_node_axis_pos]
                node_axis_neg = self.list_nodes[id_node_axis_neg]
                #
                node_axis_pos.set_neighboor(attr_name_neg, id_node_axis_neg)
                node_axis_neg.set_neighboor(attr_name_pos, id_node_axis_pos)
        
    def get_axis_name(self, dir_name):
        """
        """
        #return self.dict_dir_names.keys()[list(chain.from_iterable(dict_dir_names.values())).index(dir_name)>>1]
        return self.__dict_axis_from_dir[dir_name]

    def get_inv_dir(self, dir):
        """
        """
        return self.__dict_inv_dir[dir]
    
    def _update_valencies(self):
        """
        """
        for node in self.list_nodes:
            node.update_valency()

    def get_node(self, id_node):
        """
        """
        return self.list_nodes[id_node]
        
    def get_link(self, axis, id_link):
        """
        """
        return self.dict_links[axis][id_link]
        
    def remove_node(self, id_node):
        """
        """
        node = self.get_node(id_node)
        # pour tous les voisins du noeud a retirer
        for dir, id_neighboor in node.dict_neighboors.iteritems():
            # si le voisin existe
            if id_neighboor != -1:
                node_neighboor = self.get_node(id_neighboor)
                # remove link to neighboor
                node_neighboor.set_neighboor(self.get_inv_dir(dir), -1)
                # update valency for the neighboor
                node_neighboor.decrement_valency()
        # on met a jour les listes: noeuds actifs, retires
        self.list_ids_active_nodes.remove(id_node)
        self.list_ids_removed_nodes.append(id_node)
        
    def reduce_amount(self, node, id_node, amount):
        """
        """
        node.reduce_amount(amount)
        if not node.is_valid():
            self.remove_node(id_node)
            
    def consume_link(self, node, id_node, id_node_neighboor, amount):
        """
        """
        #
        self.reduce_amount(node, id_node, amount)
        #
        node_neighboor = self.get_node(id_node_neighboor)
        self.reduce_amount(node_neighboor, id_node_neighboor, amount)
        #
        return self.add_link(node, node_neighboor, amount)
        
    def add_link(self, node_0, node_1, amount):
        """
        """
        link = Link(node_0, node_1, amount)
        axis = link.get_axis()
        id_link = len(self.dict_links[axis])
        self.dict_links[axis].append(link)
        return (axis, id_link)
        
class APU_IA(Network):
    """
    """
    def test_with_rule_0(self, id_node):
        """
        """
        return self.get_node(id_node).valency == 1
    
    def get_amount_from_neighboor_rule_1(self, id_node_neighboor):
            return 0 if id_node_neighboor == -1 else min(2, self.get_node(id_node_neighboor).get_amount())
            
    def test_with_rule_1(self, id_node):
        """
        """
        node = self.get_node(id_node)
        list_potential_links = [self.get_amount_from_neighboor_rule_1(id_node_neighboor) for id_node_neighboor in node.dict_neighboors.itervalues()]
        potential_amount = sum(list_potential_links)
        #print >> sys.stderr, "list_potential_links: ", list_potential_links
        #print >> sys.stderr, "potential_amount: %d - ", potential_amount
        return node.get_amount() == potential_amount
        
    def get_amount_from_neighboor_rule_2(self, id_node_neighboor, amount_node):
        retour_amount = 0
        if id_node_neighboor != -1:
            node_neighboor = self.get_node(id_node_neighboor)
            amount_neighboor = node_neighboor.get_amount()
            retour_amount = min(2, amount_neighboor) - int(amount_node == amount_neighboor)
        return retour_amount
        
    def test_with_rule_2(self, id_node):
        """
        """
        node = self.get_node(id_node)
        amount_node = node.get_amount()
        list_potential_links = [self.get_amount_from_neighboor_rule_2(id_node_neighboor, amount_node) for id_node_neighboor in node.dict_neighboors.itervalues()]
        potential_amount = sum(list_potential_links)
        #print >> sys.stderr, "list_potential_links: ", list_potential_links
        #print >> sys.stderr, "amounts: %d - %d" % (potential_amount, amount_node)
        return amount_node == potential_amount

    def find_nodes_pass_test_rule_0(self):
        """            
            rule 0: Tous les nodes avec un seul voisin
        """
        return filter(self.test_with_rule_0, self.list_ids_active_nodes)
        
    def find_nodes_pass_test_rule_1(self):
        """
        rule 1: Tous les nodes dont la somme des connexions (possibles) est egale a l'amount du node (exactement)
        """
        return filter(self.test_with_rule_1, self.list_ids_active_nodes)
    
    def find_nodes_pass_test_rule_2(self):
        """
        rule 2: Tous les nodes dont la somme des connexions (possibles) est egale a l'amount du node (exactement)
        """
        return filter(self.test_with_rule_2, self.list_ids_active_nodes)
        
    def apply_rule_0(self, list_id_nodes):
        """
        """
        for id_node in list_id_nodes:
            self.apply_rule_0_on_node(self.get_node(id_node), id_node)

    def apply_rule_0_on_node(self, node, id_node):
        """
        """
        # on parcourt la liste des (ids) voisins pour le node
        for id_node_neighboor in node.dict_neighboors.itervalues():
            # si le voisin existe
            if id_node_neighboor != -1:
                # on etablit le lien
                self.consume_link(node, id_node, id_node_neighboor, node.get_amount())
                
    def apply_rule_1_on_node(self, id_node):
        """
        """
        node = self.get_node(id_node)
        # on parcourt la liste des (ids) voisins pour le node
        for id_node_neighboor in node.dict_neighboors.itervalues():
            # si le voisin existe
            if id_node_neighboor != -1:
                node_neighboor = self.get_node(id_node_neighboor)
                #
                amount = min(2, min(node.get_amount(), node_neighboor.get_amount()))
                # on etablit le lien
                self.consume_link(node, id_node, id_node_neighboor, amount)
    
    def apply_rule_2_on_node(self, id_node):
        """
        """
        node = self.get_node(id_node)
        amount_node = node.get_amount()
        # on parcourt la liste des (ids) voisins pour le node
        for id_node_neighboor in node.dict_neighboors.itervalues():
            # si le voisin existe
            if id_node_neighboor != -1:
                node_neighboor = self.get_node(id_node_neighboor)
                #
                amount = self.get_amount_from_neighboor_rule_2(id_node_neighboor, amount_node)
                # on etablit le lien
                self.consume_link(node, id_node, id_node_neighboor, amount)
                
    def consume_link(self, node, id_node, id_node_neighboor, amount):
        """
        """
        #
        (axis, id_link) = Network.consume_link(self, node, id_node, id_node_neighboor, amount)
        #
        self.apply_rule_3_on_nodes(self.get_link(axis, id_link))
        #
        APU_IA.__execute_command__(node, self.get_node(id_node_neighboor), amount)
        
    def apply_rule_3_on_nodes(self, link):
        """
        """
        axis = link.get_axis()
        for id_node in self.list_ids_active_nodes:
            node = self.get_node(id_node)
            #
            list_nodes_neighboors_to_remove = []
            for dir_neighboor, id_node_neighboor in node.dict_neighboors.iteritems():
                if id_node_neighboor != -1:
                    axis_neightboor = self.get_axis_name(dir_neighboor)
                    if axis_neightboor != axis:
                        node_neighboor = self.get_node(id_node_neighboor)
                        if link.intersect(Link(node, node_neighboor, 1)):
                            list_nodes_neighboors_to_remove.append((id_node_neighboor, dir_neighboor))
            #
            for id_node_neighboor, dir_neighboor in list_nodes_neighboors_to_remove:
                #
                node.set_neighboor(dir_neighboor, -1)
                node.decrement_valency()
                #
                node_neighboor = self.get_node(id_node_neighboor)
                node_neighboor.set_neighboor(self.get_inv_dir(dir_neighboor), -1)
                node_neighboor.decrement_valency()
    
    def get_node_with_max_sum_amount(self):
        """
        """
        def compute_sum_amount_from_neighboors(id_node):
            return sum(
                [
                    0 if id_node_neighboor == -1 else self.get_node(id_node_neighboor).get_amount() 
                    for id_node_neighboor in self.get_node(id_node).dict_neighboors.values()
                ]
            )
            
        # url: http://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
        try:
            return max(
                [
                    (
                        id_node, 
                        self.get_node(id_node).get_amount() + compute_sum_amount_from_neighboors(id_node)
                    ) 
                    for id_node in self.list_ids_active_nodes
                ],
                key=itemgetter(1)
                )[0]
        except:
            return -1
        
    def apply_rule_4(self):
        """
        """
        id_node = self.get_node_with_max_sum_amount()
        if id_node != -1:
            print >> sys.stderr, "rule_4, id_node: ", id_node
            node = self.get_node(id_node)
            amount_node = node.get_amount()
            #
            id_node_neighboor, amount_neighboor = max(
                [
                (id_node_neighboor, self.get_node(id_node_neighboor).get_amount()) 
                for id_node_neighboor in node.dict_neighboors.itervalues()
                ],
                key=itemgetter(1)
            )
            # on etablit le lien
            self.consume_link(node, id_node, id_node_neighboor, min(2, min(amount_node, amount_neighboor)))
    
    @staticmethod
    def __execute_command__(node_0, node_1, amount):
        """
        """
        print "%d %d %d %d %d" % (node_0.x, node_0.y, node_1.x, node_1.y, amount)
        
    def resolve(self):
        """
        """
        while(True):
            # rule 0
            list_nodes_rule_0 = self.find_nodes_pass_test_rule_0()
            if list_nodes_rule_0:
                print >> sys.stderr, "list_nodes_rule_0: ", list_nodes_rule_0
                self.apply_rule_0(list_nodes_rule_0)
            else:
                list_nodes_rule_1 = self.find_nodes_pass_test_rule_1()
                if list_nodes_rule_1:
                    print >> sys.stderr, "list_nodes_rule_1: ", list_nodes_rule_1
                    self.apply_rule_1_on_node(list_nodes_rule_1.pop())
                else:
                    list_nodes_rule_2 = self.find_nodes_pass_test_rule_2()
                    if list_nodes_rule_2:
                        print >> sys.stderr, "list_nodes_rule_2: ", list_nodes_rule_2
                        self.apply_rule_2_on_node(list_nodes_rule_2.pop())
                    else:
                        # consomme un/le lien avec les nodes possedant la paire d'amount la plus grande
                        # => on suppose un impact faible sur les contraintes/resolution du systeme
                        # mais on le fait progresser d'un amount 'important'
                        self.apply_rule_4()

# The machines are gaining ground. Time to show them what we're really made of...


width = int(raw_input()) # the number of cells on the X axis
height = int(raw_input()) # the number of cells on the Y axis
apu_ia = network = APU_IA(width, height)
for i in xrange(height):
    line = raw_input() # width characters, each either a number or a '.'
    #
    network.add_line(i, line)
    
network.build()

print >> sys.stderr, "network.s_grid: ", network.s_grid
print >> sys.stderr, "network.hv_grid: ", network.hv_grid
print >> sys.stderr, "network.list_nodes: "
for id_node, node in enumerate(network.list_nodes):
    print >> sys.stderr, "-> %d = %s" % (id_node, node)

# pass les tests: 01 -> 08
# todo : 
# - gestion des contraintes a ameliorer
# - gestion des contraintes de liens sur les croisements impossibles [DONE]
# - solution multiples -> initier un move si pas de regles de resolutions applicables au depart
# - probleme de topologie (voisins qui ne sont pas voisins) sur le dernier test 'expert' !!! bizarre ...
apu_ia.resolve()
