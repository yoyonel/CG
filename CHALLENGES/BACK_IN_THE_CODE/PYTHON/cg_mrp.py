import math
import operator
import sys
from collections import defaultdict

class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       url: http://www.pygame.org/wiki/2DVectorClass
       """
    __slots__ = ['x', 'y']

    def __init__(self, x_or_pair, y=None):
        if y is None:
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
            raise IndexError("Invalid subscript " + str(key) + " to Vec2d")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vec2d")

    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)

    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))

    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))

    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

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
            return Vec2d(self.x * other.x, self.y * other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x * other[0], self.y * other[1])
        else:
            return Vec2d(self.x * other, self.y * other)

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

    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)

    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)

    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)

    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)

    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)

    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)

    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # vectory functions
    def get_length_sqrd(self):
        return self.x ** 2 + self.y ** 2

    def get_length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # distance (in term of minimal cell traversed) in a grid
    def get_dist_in_grid(self):
        return max(abs(self.x), abs(self.y))

    def get_angle(self):
        if self.get_length_sqrd() == 0:
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)

    angle = property(
        get_angle, __setangle, None, "gets or sets the angle of a vector")

    def get_angle_between(self, other):
        cross = self.x * other[1] - self.y * other[0]
        dot = self.x * other[0] + self.y * other[1]
        return math.degrees(math.atan2(cross, dot))

    def normalized(self):
        length = self.length
        if length != 0:
            return self / length
        return Vec2d(self)

    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length

    def perpendicular(self):
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y / length, self.x / length)
        return Vec2d(self)

    def dot(self, other):
        return float(self.x * other[0] + self.y * other[1])


# url: http://stackoverflow.com/questions/18516299/finding-a-list-of-all-largest-open-rectangles-in-a-grid-by-only-examining-a-list
class Range:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end if end is not None else start

    def isEmpty(self):
        return self.start > self.end

    def isUnit(self):
        return self.start == self.end

    def intersect(self, other):
        return Range(max(self.start, other.start), min(self.end, other.end))

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def len(self):
        """ """
        return self.end - self.start

    def center(self):
        """ """
        return (self.end + self.start) // 2

    def clamp(self, value):
        """ """
        return max(min(value, self.end), self.start)
    
    def __repr__(self):
        return "Range(%d,%d)" % (self.start, self.end)
    
    
class ClippedGeometry(object):
    """ """
    def __init__(self):
        """ """
        

class SolveBatmanProblem(object):
    """ """
    
    def __init__(self, w, h, x, y):
        """ """
        #
        self.pos = Vec2d(x, y)
        self.cut = Vec2d(0, 0)
        #
        self.init_dims = [Range(0, w-1), Range(0, h-1)]
        self.cur_dims = [Range(0, w-1), Range(0, h-1)]
        
    def compute_next_position(self, state='UNKNOWN'):
        next_position = self.pos
        
        xRange, yRange = self.cur_dims        
        print >> sys.stderr, "xRange, yRange: ", xRange, yRange
        
        if not yRange.isUnit():
            # ligne verticale, deplacement selon l'axe Y
            next_x = self.pos.x
            #
            pos = self.pos.y
            cut = self.cut.y
            valid_domain = self.cur_dims[1]
            domain = self.init_dims[1]
            
            next_pos, next_cut, next_valid_domain = self.compute_for_1d_segment(pos, cut, state, valid_domain, domain)
            
            next_y = next_pos
            self.cut = Vec2d(self.cut.x, next_cut)
            self.cur_dims[1] = next_valid_domain
            
        elif not xRange.isUnit():
            # ligne horizontale, deplacement selon l'axe X
            next_y = yRange.start
            
            if self.pos.y != yRange.start:
                next_x = self.pos.x
            else:
                #
                pos = self.pos.x
                cut = self.cut.x
                valid_domain = self.cur_dims[0]
                domain = self.init_dims[0]
                
                next_pos, next_cut, next_valid_domain = self.compute_for_1d_segment(pos, cut, state, valid_domain, domain)
                
                next_x = next_pos
                self.cut = Vec2d(next_cut, self.cut.y)
                self.cur_dims[0] = next_valid_domain
        
        next_position = Vec2d(next_x, next_y)
        self.pos = next_position
        return next_position
    
    def compute_next_valid_domain(self, pos, cut, state, valid_domain, domain):
        """ """
        next_valid_domain = valid_domain
        if state == 'WARMER':
            if pos >= cut:
                next_valid_domain = Range(domain.clamp(cut+1), valid_domain.end)
            else:
                next_valid_domain = Range(valid_domain.start, domain.clamp(cut-1))
        elif state == 'COLDER':
            if pos < cut:
                next_valid_domain = Range(domain.clamp(cut+1), valid_domain.end)
            else:
                next_valid_domain = Range(valid_domain.start, domain.clamp(cut-1))
        return next_valid_domain            
        
    def compute_cut(self, pos, valid_domain):
        """ """
        cut = valid_domain.center()
        #offset_cut = valid_domain.len() // 8
        offset_cut = 0
        cut +=  (1 if pos > cut else -1) * offset_cut
        return cut
        
    def compute_for_1d_segment(self, pos, cut, state, valid_domain, domain):
        """ """
        next_pos = pos
        next_cut = cut
        next_valid_domain = valid_domain
        
        if valid_domain.isUnit():
            next_pos = valid_domain.start
        else:
            print >> sys.stderr, "-> pos, cut, state, valid_domain, domain: ", pos, cut, state, valid_domain, domain
            
            if state == 'SAME':
                next_pos = cut
                next_valid_domain = Range(cut, cut)
            else:
                # maj de la zone d'exploration
                next_valid_domain = self.compute_next_valid_domain(pos, cut, state, valid_domain, domain)
        
                # symetrie centrale par rapport a mid (le centre)
                mid = self.compute_cut(pos, next_valid_domain)
                print >> sys.stderr, "- mid for cutting: ", mid
                
                states_values = defaultdict(int, {'WARMER': 1, 'COLDER': -1})
                next_pos = domain.clamp(2*mid - pos)
                next_pos = domain.clamp(next_pos + (states_values[state] if next_pos == pos else 0))
                next_cut = (pos + next_pos) * 0.5
                #url: https://openclassrooms.com/forum/sujet/capturer-une-partie-entiere-avec-python
                next_pos = domain.clamp(next_pos + bool(next_cut%1))
                next_cut = (pos + next_pos) * 0.5
        return next_pos, next_cut, next_valid_domain
    

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in raw_input().split()]
n = int(raw_input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]
solver = SolveBatmanProblem(w, h, x0, y0)

# game loop
while 1:
    bomb_dist = raw_input()  # Current distance to the bomb compared to previous distance (COLDER, WARMER, SAME or UNKNOWN)
    
    next_position = solver.compute_next_position(bomb_dist)
        
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    print "%d %d" % (next_position.x, next_position.y)


