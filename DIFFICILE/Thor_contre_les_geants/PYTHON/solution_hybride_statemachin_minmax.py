import sys
import math
import operator

# limites de la grille/plateau de jeux/deplacements (pour Thor et le Geants)
max_width, max_height = 40, 18
max_dist_sqrd = max_width**2 + max_height**2
max_dist_in_grid = max(max_width, max_height)

# url: http://gamedev.stackexchange.com/questions/49290/whats-the-best-way-of-transforming-a-2d-vector-into-the-closest-8-way-compass-d
dict_dir = {
	(-1, -1): 'NW',
	(-1, 0): 'W',
	(-1, 1): 'SW',
	(0, -1): 'N',
	(0, 0): 'WAIT',
	(0, 1): 'S',
	(1, -1): 'NE',
	(1, 0): 'E',
	(1, 1): 'SE',
}
# url: http://stackoverflow.com/questions/483666/python-reverse-inverse-a-mapping
inv_dict_dir = {v: k for k, v in dict_dir.items()}

# url: http://www.pygame.org/wiki/2DVectorClass
class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']
 
    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
 
    def __len__(self):
        return 2
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__
 
    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
        
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
    
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__
 
    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self
        
    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2
        
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
        
    # distance (in term of minimal cell traversed) in a grid
    def get_dist_in_grid(self):
        return max(abs(self.x), abs(self.y))
        
def GetDirection(heading):
	inv_max_coordXY = 1.0 / max(abs(heading.x), abs(heading.y))
	tuple_imaginary = (round(heading.x*inv_max_coordXY), round(heading.y*inv_max_coordXY))
	return dict_dir[tuple_imaginary]

def GetDirectionFromPositions(pos_origin, pos_dest):
    return GetDirection(pos_dest - pos_origin)

def GetVec2DFromDirection(dir):
	return inv_dict_dir[dir]

def ComputeNextPosition(cur_position, dst_position):
	return cur_position + GetVec2DFromDirection(GetDirectionFromPositions(cur_position, dst_position))

def ComputePositionAfterCommand(cur_position, command):
    vec_offset = Vec2d(0, 0) if command == "STRIKE" else GetVec2DFromDirection(command)
    return cur_position + vec_offset
    
def EvaluateCommandForMoving(cmd, thor_pos, giants_pos):
    """
    """
    next_thor_pos = ComputePositionAfterCommand(thor_pos, cmd)
    #print >> sys.stderr, "cmd: %s - thor_pos:%s - next_thor_pos:%s - giants_pos: %s" % (cmd, thor_pos, next_thor_pos, giants_pos)
    dists_thor_from_giants = [ (giant_pos - next_thor_pos).get_dist_in_grid() for giant_pos in giants_pos ]
    #print >> sys.stderr, "dists_thor_from_giants: ", dists_thor_from_giants
    dists_0_thor_giants = [0 for d in dists_thor_from_giants if d <= 1]
    evaluation = len(dists_0_thor_giants)*max_dist_in_grid if dists_0_thor_giants else sum(dists_thor_from_giants)/len(giants_pos)
    # next position en dehors des limites du plateau ?
    if (next_thor_pos.x < 0) | (next_thor_pos.x > max_width) | (next_thor_pos.y < 0) | (next_thor_pos.y > max_height):
        # si oui "gros" malus sur le deplacement (ne devrait pas etre choisi au final)
        evaluation += max_dist_in_grid*max_dist_in_grid*len(giants_pos)
    return evaluation

def EvaluateCommandForStriking(thor_pos, giants_pos):
    """
    return
        < 0 : si un geant (au moins) atteint thor au prochain coup (avec la commande cmd)
            -> - n (n: nombre de geants qui ont atteint thor)
        > 0 : si aucun geant n'atteint thor (tout va bien)
            -> Nombre de geants blastes par le strike
            => plus c'est grand mieux c'est ! (Thor tue plus de geants)
    """
    vecs_thor_from_giants = [ giant_pos - thor_pos for giant_pos in giants_pos ]
    dists_thor_from_giants = [ vec_thor_giant.get_length_sqrd() for vec_thor_giant in vecs_thor_from_giants ]
    giants_blast = [ 1 for vec_thor_giant in vecs_thor_from_giants if (abs(vec_thor_giant.x) < 5) & (abs(vec_thor_giant.y) < 5) ]
    dists_0_thor_giants = [0 for d in dists_thor_from_giants if d == 0]
    evaluation = - len(dists_0_thor_giants) if dists_0_thor_giants else giants_blast.count(1)
    return evaluation

def get_elements_from_filter(_iter, _op_filter, _func_key_for_filter, _func_filter_on_result):
    #
    one_filter_element = _op_filter(_iter, key=_func_key_for_filter)
    filter_value = _func_key_for_filter(one_filter_element)
    return [_func_filter_on_result(filter_element) for filter_element in _iter if _func_key_for_filter(filter_element) == filter_value]

def compute_command(thor_pos, giants_pos):
    #
    
    vec2d_offset = Vec2d(0,0)
    
    # on evalue le nombre de geants tues par un strike
    nb_strikes = EvaluateCommandForStriking(thor_pos, giants_pos)
    #print >> sys.stderr, "nb_strikes: ", nb_strikes
    
    # si le nombre de tues est egale au nombre de geant
    if nb_strikes == n:
        # la partie est (sera) finie
        cmd = "STRIKE"
    else:
        # on evalue les moves possibles pour thor (wait et directions cardinales)
        # on recupere:
        # - une evaluation par rapport aux distances entre thor et les geants (avec mallus si un geant tue thor)
        # - une evaluation du nombre de geants tues au prochain tour avec les moves
        evaluations_for_moving = [
            (
                EvaluateCommandForMoving(cmd, thor_pos, giants_pos),
                EvaluateCommandForStriking(ComputePositionAfterCommand(thor_pos, cmd), giants_pos),
                cmd, 
                vec_offset
                )
            for cmd, vec_offset in inv_dict_dir.iteritems()
        ]
        # on filtre cet evaluation pour retirer les possibilites de move qui conduirait thor a une mort certaine
        evaluations_for_moving = filter(lambda x: x[0] < max_dist_in_grid, evaluations_for_moving)
        
        # est ce qu'on peut (encore) se deplacer ?
        if bool(evaluations_for_moving):
            # on calcul le barycentre de position des geants
            barycenter = sum(giants_pos) * (1.0/len(giants_pos))
            dir = GetDirectionFromPositions(thor_pos, barycenter)
            # on test si on peut deplacer thor vers ce barycentre
            # i.e. => on se deplacant on ne rencontre (potentiellement) aucun geant !
            if EvaluateCommandForMoving(dir, thor_pos, giants_pos) < max_dist_in_grid:
                # si oui on deplace thor
                vec2d_offset = GetVec2DFromDirection(dir)
                cmd = dir
            else:
                # si non on cherche le move (tuple) qui maximise le strike
                moves_for_max_strikes = get_elements_from_filter(evaluations_for_moving, max, operator.itemgetter(1), lambda x:x)
                
                # critere de deplacement sur le barycentre des positions des geants
                # en optant pour le max -> on privilige les diagonales !
                moves_with_dist_to_barycenter = [ ((barycenter - (thor_pos + tuple[3])).get_length_sqrd(), tuple) for tuple in moves_for_max_strikes ]
                moves_for_max_dist_to_bary = get_elements_from_filter(moves_with_dist_to_barycenter, max, operator.itemgetter(0), operator.itemgetter(1))
                
                # a ce niveau tout les deplacements possibles se valent
                # on recupere le 1er deplacement de la liste
                eval_move, eval_strike, cmd_for_max_strikes, vec_move = moves_for_max_dist_to_bary.pop()
                
                # on deplace thor
                vec2d_offset = vec_move
                cmd = cmd_for_max_strikes
        else:
            # si non on strike (sinon on perd au prochain tour)
            # position de Thor inchangee
            cmd = "STRIKE"
        
    thor_pos += vec2d_offset
    
    return (cmd, thor_pos)
    
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

tx, ty = [int(i) for i in raw_input().split()]

thor_pos = Vec2d(tx, ty)

# game loop
while 1:
    cmd = "WAIT"
    
     # h: the remaining number of hammer strikes.
     # n: the number of giants which are still present on the map.
    h, n = [int(i) for i in raw_input().split()]
    
    #print >> sys.stderr, "thor_pos: ", thor_pos
    
    # on conserve les positions courantes des geants
    giants_pos = [None] * n
    for i in xrange(n):
        x, y = [int(j) for j in raw_input().split()]
        giants_pos[i] = Vec2d(x, y)

    cmd, thor_pos = compute_command(thor_pos, giants_pos)
    
    print cmd

