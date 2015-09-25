import sys
import math
import itertools
import operator

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
        return self.x**2 + self.y**2
        
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
        
    # distance (in term of minimal cell traversed) in a grid
    def get_dist_in_grid(self):
        return max(abs(self.x), abs(self.y))
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
        
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")
 
    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))
 
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
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
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)
 
    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])
        

#url: https://www.pygame.org/wiki/IntersectingLineDetection?parent=CookBook
# Calc the gradient 'm' of a line between p1 and p2
def calculateGradient(p1, p2):
  
   # Ensure that the line is not vertical
   if (p1[0] != p2[0]):
       m = (p1[1] - p2[1]) / (p1[0] - p2[0])
       return m
   else:
       return None
 
# Calc the point 'b' where line crosses the Y axis
def calculateYAxisIntersect(p, m):
   return  p[1] - (m * p[0])
 
# Calc the point where two infinitely long lines (p1 to p2 and p3 to p4) intersect.
# Handle parallel lines and vertical lines (the later has infinate 'm').
# Returns a point tuple of points like this ((x,y),...)  or None
# In non parallel cases the tuple will contain just one point.
# For parallel lines that lay on top of one another the tuple will contain
# all four points of the two lines
def getIntersectPoint(p1, p2, p3, p4):
   m1 = calculateGradient(p1, p2)
   m2 = calculateGradient(p3, p4)
      
   # See if the the lines are parallel
   if (m1 != m2):
       # Not parallel
      
       # See if either line is vertical
       if (m1 is not None and m2 is not None):
           # Neither line vertical           
           b1 = calculateYAxisIntersect(p1, m1)
           b2 = calculateYAxisIntersect(p3, m2)   
           x = (b2 - b1) / (m1 - m2)       
           y = (m1 * x) + b1           
       else:
           # Line 1 is vertical so use line 2's values
           if (m1 is None):
               b2 = calculateYAxisIntersect(p3, m2)   
               x = p1[0]
               y = (m2 * x) + b2
           # Line 2 is vertical so use line 1's values               
           elif (m2 is None):
               b1 = calculateYAxisIntersect(p1, m1)
               x = p3[0]
               y = (m1 * x) + b1           
           else:
               assert false
              
       return ((x,y),)
   else:
       # Parallel lines with same 'b' value must be the same line so they intersect
       # everywhere in this case we return the start and end points of both lines
       # the calculateIntersectPoint method will sort out which of these points
       # lays on both line segments
       b1, b2 = None, None # vertical lines have no b value
       if m1 is not None:
           b1 = calculateYAxisIntersect(p1, m1)
          
       if m2 is not None:   
           b2 = calculateYAxisIntersect(p3, m2)
      
       # If these parallel lines lay on one another   
       if b1 == b2:
           return p1,p2,p3,p4
       else:
           return None
           
class Grid:
    #
    def __init__(self, w, h):
        #
        self.origin = Vec2d(0, 0)
        self.dim = Vec2d(w-1, h-1)
        self.initial_dim = self.dim
        #print >> sys.stderr, "self.initial_dim: ", self.initial_dim
        #
        self.center = Vec2d(w/2, h/2)
        #
        self.list_corners = [] 
        #
        self.__init_list_corners__()
        #
        self.sorting_corners()
    
    def __init_list_corners__(self):
        #
        self.list_corners.append(self.origin)
        self.list_corners.append(self.origin + Vec2d(0, self.dim.y))
        self.list_corners.append(self.origin + Vec2d(self.dim.x, self.dim.y))
        self.list_corners.append(self.origin + Vec2d(self.dim.x, 0))
        
    def sorting_corners(self):
        #
        self.list_corners = sorted(self.list_corners, key=lambda corner: (corner - self.center).get_angle())
    
    def update_center(self):
        #
        self.center = sum(self.list_corners) / len(self.list_corners)
        
    def is_outside(self, pos):
        #
        return (pos.x < 0) | (pos.y < 0) | (pos.x > self.initial_dim.x) | (pos.y > self.initial_dim.y)
        
    def clip(self, p0, p1):
        #
        # p0: inside grid
        #
        #>>> grid = Grid(10, 10); grid.clip(grid.center, Vec2d(15, 5))
        #((9, 5),)
        #
        list_intersections = [getIntersectPoint(p0, p1, p2, p3) for p2, p3 in zip(self.list_corners, self.list_corners[1:])]
        list_intersections.append(getIntersectPoint(p0, p1, self.list_corners[-1], self.list_corners[0]))
        vec_p0p1 = p1 - p0
        dot2_p0p1 = vec_p0p1.dot(vec_p0p1)
        def func_filter(intersection):
            retour = False
            if intersection:
                intersection = intersection[0]
                vec_center_to_intersection = intersection - self.center
                dot = vec_p0p1.dot(vec_center_to_intersection)
                retour = (dot >= 0) & (dot <= dot2_p0p1)
            return retour
        list_intersections = filter(func_filter, list_intersections)
        try:
            return list_intersections[0]
        except:
            return ()
    
    def clip_from_center(self, p):
        #
        #>>> grid = Grid(10, 10); grid.clip_from_center(Vec2d(15, 5))
        #(9, 5)
        #
        try:
            return self.clip(self.center, p)[0]
        except:
            return ()
        
    def compute_position_for_splitting(self, last_pos):
        #
        new_pos = 2*self.center - last_pos
        print >> sys.stderr, "self.center: ", self.center
        print >> sys.stderr, "last_pos: ", last_pos
        print >> sys.stderr, "new_pos: ", new_pos
        #
        if self.is_outside(new_pos):
            # on calcul l'intersection entre le segment reliant le centre et la nouvelle
            # et les bords de la grille (initiale)
            new_pos = self.clip_from_center(new_pos)
        #
        print >> sys.stderr, "new_pos: ", new_pos
        return new_pos
        
    def split_with_median(self, p0, p1):
        #
        # We split our grid by the median between p0 and p1.
        # p0, p1 in the grid
        # p0: is in the 'positiv' plane (we keep this plane)
        #
        # compute the median 
        # position : self.center
        # direction : perpendicular (normal) of [p0, p1]
        p0p1 = p1 - p0
        n_p0p1 = p0p1.perpendicular()
        centerp0 = p0 - self.center
        # reconstruct the new grid
        def is_in_positiv_plane(corner):
            centerp0.dot(corner - self.center) >= 0
        filter_list_corners = [(corner, centerp0.dot(corner - self.center)) for corner in self.list_corners]
        list_edges_grid = zip(filter_list_corners, filter_list_corners[1:])
        list_edges_grid.append((filter_list_corners[-1], filter_list_corners[0]))
        list_intersections = [ getIntersectPoint(e0[0], e1[0], self.center, self.center + n_p0p1) for e0, e1 in list_edges_grid if e0[1]*e1[1] < 0]
        list_intersections = [ Vec2d(intersection[0]) for intersection in list_intersections if intersection ]
        #print >> sys.stderr, "filter_list_corners: ", filter_list_corners
        #print >> sys.stderr, "list_edges_grid: ", list_edges_grid
        #print >> sys.stderr, "list_intersections: ", list_intersections
        self.list_corners = [tuple_corner[0] for tuple_corner in filter_list_corners if tuple_corner[1] >= 0]
        self.list_corners += list_intersections
        #print >> sys.stderr, "list_corners:", self.list_corners
        #
        self.sorting_corners()
        self.update_center()
        #
        #print >> sys.stderr, "center:", self.center
        
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

 # w: width of the building.
 # h: height of the building.
w, h = [int(i) for i in raw_input().split()]
n = int(raw_input()) # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]
x_bat, y_bat = x0, y0
grid = Grid(w, h)

# game loop
while 1:
    bomb_dist = raw_input() # Current distance to the bomb compared to previous distance (COLDER, WARMER, SAME or UNKNOWN)
    
    if bomb_dist == 'UNKNOWN':
        x_bat, y_bat = grid.compute_position_for_splitting(Vec2d(x0, y0))
    elif bomb_dist == 'WARMER':
        # on "decoupe" la grille
        grid.split_with_median(Vec2d(x_bat, y_bat), Vec2d(x0, y0))
        # nouveau split
        x0, y0 = x_bat, y_bat
        x_bat, y_bat = grid.compute_position_for_splitting(Vec2d(x_bat, y_bat))
    elif bomb_dist == 'COLDER':
        # on "decoupe" la grille
        grid.split_with_median(Vec2d(x0, y0), Vec2d(x_bat, y_bat))
        # nouveau split
        x0, y0 = x_bat, y_bat
        x_bat, y_bat = grid.compute_position_for_splitting(Vec2d(x_bat, y_bat))
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    #print "0 0"
    print "%d %d" % (x_bat, y_bat)
