import sys
import math
import itertools
import operator

# url: https://www.pygame.org/wiki/IntersectingLineDetection?parent=CookBook
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
    return p[1] - (m * p[0])


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
                assert False

        return ((x, y),)
    else:
        # Parallel lines with same 'b' value must be the same line so they intersect
        # everywhere in this case we return the start and end points of both lines
        # the calculateIntersectPoint method will sort out which of these points
        # lays on both line segments
        b1, b2 = None, None  # vertical lines have no b value
        if m1 is not None:
            b1 = calculateYAxisIntersect(p1, m1)

        if m2 is not None:
            b2 = calculateYAxisIntersect(p3, m2)

        # If these parallel lines lay on one another
        if b1 == b2:
            return p1, p2, p3, p4
        else:
            return None


def liesOnSegment(a, b, c):
    dotProduct = (c.x - a.x) * (c.x - b.x) + (c.y - a.y) * (c.y - b.y)
    return dotProduct < 0


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


class Grid(object):
    """ """

    def __init__(self, w, h):
        """
        :param w:
        :param h:
        :return:
        """
        self.origin = Vec2d(0, 0)
        self.dim = Vec2d(w - 1, h - 1)
        self.initial_dim = self.dim
        #
        self.center = Vec2d(w // 2, h // 2)
        #
        self.list_corners = []
        self.list_borders = []
        #
        self.__init_list_corners__()
        self._sorting_corners_()
        #
        self._update_borders_()

    def __init_list_corners__(self):
        """

        :return:
        """
        self.list_corners.append(self.origin)
        self.list_corners.append(self.origin + Vec2d(0, self.dim.y))
        self.list_corners.append(self.origin + Vec2d(self.dim.x, self.dim.y))
        self.list_corners.append(self.origin + Vec2d(self.dim.x, 0))
        # on decale de (0.5, 0.5) pour placer les bords sur les centres des cases
        self.list_corners = [
            corner + Vec2d(0.5, 0.5) for corner in self.list_corners
        ]

    def _sorting_corners_(self):
        """

        :return:
        """
        self.list_corners = sorted(
            self.list_corners,
            key=lambda corner: (corner - self.center).get_angle()
        )

    def _update_borders_(self):
        """

        :return:
        """
        self.list_borders = zip(self.list_corners, self.list_corners[1:])
        self.list_borders.append((self.list_corners[-1], self.list_corners[0]))

    def _update_center_(self):
        """

        :return:
        """
        self.center = sum(self.list_corners) / len(self.list_corners)

    def update(self):
        """

        :return:
        """
        self._sorting_corners_()
        self._update_borders_()
        self._update_center_()

    def is_outside(self, pos):
        """

        :param pos:
        :return:
        """
        return (pos.x < 0) | (pos.y < 0) | (pos.x > self.initial_dim.x) | (pos.y > self.initial_dim.y)

    def get_intersections_by_line(self, p0, p1):
        """

        :param p0: 1er point appartenant a la ligne d'intersection
        :param p1: 2nd point appartenant a la ligne d'intersection
        :return:
        >>> grid = Grid(10.0, 10.0); grid.get_intersections_by_line(Vec2d(3.0, -2.0), Vec2d(9.0, 15.0))
         Out[179]:
         [(Vec2d(6.88235294118, 9.0), Vec2d(0, 9.0), Vec2d(9.0, 9.0)),
         (Vec2d(3.70588235294, 0.0), Vec2d(9.0, 0), Vec2d(0, 0))
        """
        list_intersections = [
            getIntersectPoint(p0, p1, p2, p3) for p2, p3 in self.list_borders
        ]

        list_intersections = zip(list_intersections, self.list_borders)
        list_intersections = map(
            lambda x: (Vec2d(x[0][0]), x[1][0], x[1][1]),
            filter(lambda x: x[0], list_intersections)
        )

        def func_filter(tuple_intersection):
            point_intersection, e0, e1 = tuple_intersection
            return liesOnSegment(e0, e1, point_intersection)

        return filter(func_filter, list_intersections)

    def clip_by_line(self, p0, p1):
        """

        :param p0:
        :param p1:
        :return:
        """
        intersections = self.get_intersections_by_line(p0, p1)
        points_intersections = map(lambda x: x[0], intersections)
        #
        vec_p0p1 = p1 - p0
        n_p0p1 = vec_p0p1.perpendicular()
        #
        self.list_corners = filter(
            lambda c: n_p0p1.dot(c - p0) >= 0.0,
            self.list_corners + points_intersections
        )
        self.update()


class SolveBatmanProblem(Grid):
    def __init__(self, x, y, w, h):
        super(SolveBatmanProblem, self).__init__(w, h)
        self.bat_pos = Vec2d(x, y)
        self.bat_last_pos = None

    def compute_next_position(self, state='UNKNOWN'):
        pass



