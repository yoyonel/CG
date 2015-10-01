import sys
from collections import defaultdict
import random   # url: https://docs.python.org/2/library/random.html#module-random
import heapq
import math
import operator


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

    def __setlength(self, value):
        length = self.get_length()
        self.x *= value / length
        self.y *= value / length

    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec2d(x, y)

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

    def __repr__(self):
        return "Range(%d,%d)" % (self.start, self.end)


class Rect:
    def __init__(self, _xRange, _yRange):
        self.xRange = _xRange
        self.yRange = _yRange

    def isEmpty(self):
        return self.xRange.isEmpty() or self.yRange.isEmpty()

    def isUnit(self):
        return self.xRange.isUnit() and self.yRange.isUnit()

    # def intersect(self, other):
    #    return Range(max(self.start, other.start), min(self.end, other.end))

    def contains(self, other):
        return self.xRange.contains(other.xRange) and self.yRange.contains(other.yRange)

    def area(self):
        """ """
        return self.xRange.len() * self.yRange.len()

    def center(self):
        """ """
        return self.xRange.center(), self.yRange.center()

    def isInside(self, pos):
        """ pos = (x, y) """
        return self.contains(Rect(Range(pos[0], pos[0]), Range(pos[1], pos[1])))

    def isOnBorder(self, pos):
        """ """
        return (pos[0] == self.xRange.start) | \
               (pos[0] == self.xRange.end) | \
               (pos[1] == self.yRange.start) | \
               (pos[1] == self.yRange.end)

    def minX(self):
        """ """
        return self.xRange.start

    def maxX(self):
        """ """
        return self.xRange.end

    def minY(self):
        """ """
        return self.yRange.start

    def maxY(self):
        """ """
        return self.yRange.end

    def coordinate(self, _pos):
        """ """
        leftupper_corner = (self.minX(), self.minY())
        return _pos[0] - leftupper_corner[0], _pos[1] - leftupper_corner[1]

    def toWorld(self, _pos):
        """ """
        leftupper_corner = (self.minX(), self.minY())
        return _pos[0] + leftupper_corner[0], _pos[1] + leftupper_corner[1]

    def corners(self):
        """ """
        return (
            (self.minX(), self.minY()),
            (self.maxX(), self.minY()),
            (self.maxX(), self.maxY()),
            (self.minX(), self.maxY()),
        )

    def __repr__(self):
        return "Rect(%s,%s)" % (self.xRange, self.yRange)


def intersect(a, b):
    r = Rect(Range(b.xRange.start, a.xRange.end), a.yRange.intersect(b.yRange))
    brokenB = not a.yRange.contains(b.yRange)
    fullyAbsorbedA = b.yRange.contains(a.yRange)
    return r, brokenB, fullyAbsorbedA


def findOpenRectangles(freeElements, pastRowNum):
    # From `freeElements`, compute free runs into `freeRunsPerRow`
    from collections import defaultdict

    freeRunsPerRow = defaultdict(set)
    rowNum = -1
    currRun = None
    for fe in freeElements:
        if fe[0] != rowNum:
            if currRun is not None:
                freeRunsPerRow[rowNum] |= {Rect(Range(rowNum), currRun)}
            currRun = Range(fe[1], fe[1])
            rowNum = fe[0]
        elif fe[1] == currRun.end + 1:
            currRun = Range(currRun.start, fe[1])
        else:
            freeRunsPerRow[rowNum] |= {Rect(Range(rowNum), currRun)}
            currRun = Range(fe[1], fe[1])
    if currRun is not None:
        freeRunsPerRow[rowNum] |= {Rect(Range(rowNum), currRun)}
        currRun = None
    # for freeRuns in freeRunsPerRow.items():
    #    print(freeRuns)

    # Yield open rectangles
    currRects = set()
    for currRow in range(0, pastRowNum):
        continuingRects = set()
        startingRects = set(freeRunsPerRow[currRow])
        for b in currRects:
            brokenB = True
            for a in freeRunsPerRow[currRow]:
                modifiedContinuingRect, t_brokenB, t_absorbedA = intersect(a, b)
                if not modifiedContinuingRect.isEmpty() and not [x for x in continuingRects if
                                                                 x.contains(modifiedContinuingRect)]:
                    continuingRects -= {x for x in continuingRects if modifiedContinuingRect.contains(x)}
                    continuingRects |= {modifiedContinuingRect}
                if not t_brokenB:
                    brokenB = False
                if t_absorbedA:
                    startingRects -= {a}
            if brokenB and not b.isUnit():
                yield b
        currRects = continuingRects
        currRects |= startingRects
    for b in currRects:
        if not b.isUnit():
            yield b


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


class Border:
    """ """
    Type = Enum(["HORIZONTAL", "VERTICAL"])

    def __init__(self, _offset=0, _type=Type.HORIZONTAL):
        """ """
        self.offset = _offset
        self.type = _type

    def projection(self, _pos):
        """ """
        return [_pos[0], self.offset] if self.type == self.Type.HORIZONTAL else [self.offset, _pos[1]]

    def distance(self, _pos):
        """ """
        return abs(_pos[int(self.type == self.Type.HORIZONTAL)] - self.offset)

    def __repr__(self):
        """ """
        return "(%d, %s)" % (self.offset, self.type)


class Board(object):
    """ """
    cardinals = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    # cardinals = [(x, y) for y in xrange(-1, 2) for x in xrange(-1, 2) if bool(x) | bool(y)]

    def __init__(self, _l=35, _h=20):
        """ """
        self.l = _l
        self.h = _h
        self.center = (_l // 2, _h // 2)
        self.board = ['.' * _l] * _h

    def update(self, _i_line, _line):
        """ """
        self.board[_i_line] = _line

    @staticmethod
    def distance(_pos0, _pos1):
        """
         Manhattan distance
        """
        return abs(_pos1[0] - _pos0[0]) + abs(_pos1[1] - _pos0[1])

    def projections_to_borders(self, _pos):
        """ """
        return [
            (0, _pos[1]),  # WEST BORDER
            (self.l - 1, _pos[1]),  # EAST BORDER
            (_pos[0], 0),  # NORTH BORDER
            (_pos[0], self.h - 1),  # SOUTH BORDER
        ]

    def distances_to_borders(self, _pos):
        """ """
        l_pos = [_pos] * 4
        proj_to_borders = self.projections_to_borders(_pos)
        return zip(map(lambda tup: self.distance(tup[0], tup[1]), zip(proj_to_borders, l_pos)), proj_to_borders)

    def get_border_from_direction(self, _str_direction):
        """ """
        if _str_direction == 'NORTH':
            return Border(0, Border.Type.HORIZONTAL)
        elif _str_direction == 'SOUTH':
            return Border(self.h - 1, Border.Type.HORIZONTAL)
        elif _str_direction == 'WEST':
            return Border(0, Border.Type.VERTICAL)
        else:  # 'EAST'
            return Border(self.l - 1, Border.Type.VERTICAL)

    def get_cell(self, _pos):
        """ """
        return self.board[_pos[1]][_pos[0]]

    def cell_available(self, _pos):
        """ """
        return self.board[_pos[1]][_pos[0]] == '.'

    def on_board(self, _pos):
        """ """
        return (0 <= _pos[0] <= (self.l - 1)) & (0 <= _pos[1] <= (self.h - 1))

    def get_neighboors(self, _pos):
        """ """
        return filter(self.on_board, [(_pos[0] + card[0], _pos[1] + card[1]) for card in self.cardinals])

    def get_neighboors_available(self, _pos):
        """ """
        return filter(self.cell_available, self.get_neighboors(_pos))

    def cells_close_to_id(self, _pos, _id):
        """ """
        return filter(lambda cell: self.get_cell(cell) == _id, self.get_neighboors(_pos))

    def is_cell_close_to_id(self, _pos, _id):
        """ """
        return bool(self.cells_close_to_id(_pos, _id))

    def get_cells_available_close_to_id(self, _id):
        """ """
        return filter(lambda cell: self.is_cell_close_to_id(cell, _id), self.get_cells_available())

    def get_cells(self):
        return [
            (colNum, rowNum)
            for rowNum, row in enumerate(self.board)
            for colNum, element in enumerate(row)
        ]

    def get_cells_filtered(self, _filter):
        """ """
        return filter(_filter, self.get_cells())

    def get_cells_possessed_by_id(self, _id):
        """ """
        return self.get_cells_filtered(lambda pos: self.board[pos[1]][pos[0]] == _id)

    def get_cells_available(self):
        """ """
        return self.get_cells_possessed_by_id('.')

    def get_cells_available_or_possessed_by_id(self, _id):
        """ """
        return self.get_cells_filtered(
            lambda pos: (self.board[pos[1]][pos[0]] == _id) | (self.board[pos[1]][pos[0]] == '.')
        )

    def random_position_available(self):
        """ """
        # list des positions disponibles
        positions_availables = self.get_cells_available()
        return positions_availables[int(random.random() * (len(positions_availables) - 1))]

    def connectivity_to_id(self, _pos, _id):
        """ """
        return len(self.cells_close_to_id(_pos, _id))

    # interface for PathFinding algo (A*, Dijkstra)
    def cost(self, a, b):
        """ """
        return 1

    def neighbors(self, a):
        """ """
        return self.get_neighboors_available(a)

    def compute_nearest_position_on_border_for_rect(self, _pos, _rect):
        """ """
        _pos = _pos[::-1]
        relativ_pos = _rect.coordinate(_pos)
        #print >> sys.stderr, "_pos: ", _pos
        #print >> sys.stderr, "relativ_pos: ", relativ_pos
        if _rect.isInside(_pos):
            pos_on_border = _rect.toWorld(
                min(
                    (
                        (relativ_pos[0], (_rect.minX(), _pos[1])),
                        (_rect.maxX() - relativ_pos[0], (_rect.maxX(), _pos[1])),
                        (relativ_pos[1], (_pos[0], _rect.minY())),
                        (_rect.maxY() - relativ_pos[1], (_pos[1], _rect.maxY()))
                    ),
                    key=lambda tup: tup[0])[1]
            )
        else:
            if relativ_pos[0] < 0:
                if relativ_pos[1] < 0:
                    pos_on_border = (_rect.minX(), _rect.minY())
                elif relativ_pos[1] > _rect.maxY():
                    pos_on_border = (_rect.minX(), _rect.maxY())
                else:
                    pos_on_border = (_rect.minX(), _pos[1])
            elif relativ_pos[0] > _rect.maxX():
                if relativ_pos[1] < 0:
                    pos_on_border = (_rect.maxX(), _rect.minY())
                elif relativ_pos[1] > _rect.maxY():
                    pos_on_border = (_rect.maxX(), _rect.maxY())
                else:
                    pos_on_border = (_rect.maxX(), _pos[1])
            else:
                if relativ_pos[1] < 0:
                    pos_on_border = (_pos[0], _rect.minY())
                else:
                    pos_on_border = (_pos[0], _rect.maxY())

        return pos_on_border[::-1]


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

# url: http://www.redblobgames.com/pathfinding/a-star/implementation.html
def a_star_search(graph, start, goal):
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
                priority = new_cost + heuristic(goal, next)
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


class MapForFloodFilling:
    #
    def __init__(self, l, h):
        #
        self.l = l
        self.h = h
        #
        self.tiles = []
        #
        self.row_init_ids = [0] * l
        #
        self.cur_id = 1
        # url: http://stackoverflow.com/questions/2626059/python-dictionary-add-or-increment-entry
        self.area_for_id = defaultdict(int)

    def append_row(self, row):
        #
        self.tiles.append(zip(row, self.row_init_ids))

    def valid_coordinates(self, x, y):
        #
        return (x >= 0) & (x < self.l) & (y >= 0) & (y < self.h)

    def get_tile(self, x, y):
        #
        return self.tiles[y][x]

    def get_tile_type(self, x, y):
        #
        return self.get_tile(x, y)[0]

    def get_tile_id(self, x, y):
        #
        return self.get_tile(x, y)[1]

    def validate_coordinates(self, x, y):
        #
        return (x, y) if self.valid_coordinates(x, y) else None

    def tile_has_id(self, x, y):
        #
        return self.get_tile_id(x, y) != 0

    def set_id(self, x, y, id):
        #
        self.tiles[y][x] = (self.tiles[y][x][0], id)
        #
        self.area_for_id[id] += 1

    def get_neighboors_coords(self, x, y):
        #
        list_neighboors_coords = (
            self.validate_coordinates(x - 1, y),
            self.validate_coordinates(x + 1, y),
            self.validate_coordinates(x, y - 1),
            self.validate_coordinates(x, y + 1)
        )
        return filter(lambda coord: coord, list_neighboors_coords)

    def get_valid_neighboors_coords_with_no_id(self, x, y):
        #
        list_neighboors_tiles = self.get_neighboors_coords(x, y)

        #
        def validate_tile(x, y):
            return (self.get_tile_type(x, y) == '.') & (not self.tile_has_id(x, y))

        #
        return filter(lambda coord: validate_tile(coord[0], coord[1]), list_neighboors_tiles)

    def update_id_for_one_tile(self, x, y):
        # set un id a une tile et renvoie les voisins (directs) sans ids (et non '#')
        tile_id = self.get_tile_id(x, y)
        #
        list_neighboors = self.get_valid_neighboors_coords_with_no_id(x, y)
        for coord in list_neighboors:
            self.set_id(coord[0], coord[1], tile_id)

        return list_neighboors

    def update_id_with_propagation(self, x, y):
        #
        self.set_id(x, y, self.cur_id)
        list_coords = [(x, y)]
        while list_coords:
            coord = list_coords.pop()
            list_neighboors = self.update_id_for_one_tile(coord[0], coord[1])
            list_coords.extend(list_neighboors)

    def get_area(self, x, y):
        #
        return self.area_for_id[self.get_tile_id(x, y)]


class Player:
    """ """

    def __init__(self, _indice, _position=(0, 0), _back_in_time_left=1):
        """ """
        self.indice = _indice
        self.position = _position
        self.back_in_time_left = _back_in_time_left

    def update_position(self, _position):
        """ """
        self.position = _position

    def update_back_in_time_left(self, _back_in_time_left):
        """ """
        self.back_in_time_left = _back_in_time_left


class GameState(object):
    """ """

    def __init__(self, _opponent_count=2):
        """ """
        #
        self.me = Player(0)
        #
        self.opponent_count = _opponent_count
        self.opponents = []
        for indice_opponent in xrange(1, opponent_count + 1):
            self.opponents.append(Player(indice_opponent))
        #
        self.board = Board()
        #
        self.game_round = 0
        #
        self.cur_rect = None

    def update_game_round(self, _game_round):
        """ """
        self.game_round = _game_round

    def update_me(self, _x, _y, _back_in_time_left):
        """
        :param _x:
        :param _y:
        :param _back_in_time_left:
        :return:
        """
        self.me.update_position((_x, _y))
        self.me.update_back_in_time_left(_back_in_time_left)

    def update_opponent(self, _indice_opponent, _x, _y, _opponent_back_in_time_left):
        """
        :param _indice_opponent:
        :param _x:
        :param _y:
        :param _opponent_back_in_time_left:
        :return:
        """
        self.opponents[_indice_opponent].update_position((_x, _y))
        self.opponents[_indice_opponent].update_back_in_time_left(_opponent_back_in_time_left)

    def update_board(self, _i_line, _line):
        """
        :param _i_line:
        :param _line:
        :return:
        """
        self.board.update(_i_line, _line)


class GameStrategy(GameState):
    """
    """
    CycleDirections = ['NORTH', 'WEST', 'SOUTH', 'EAST']

    def __init__(self, *args):
        """ """
        super(GameStrategy, self).__init__(*args)
        # 1ere destination le centre de la map
        self.destination = self.board.center
        #
        self.state = 0
        #
        self.indice_cycle_direction = 0

    @staticmethod
    def format_output(_destination):
        """
        :return:
        """
        return "%d %d" % (_destination[0], _destination[1])

    def next_move(self):
        """ """
        pos = self.me.position

        if self.state == 0:
            # 1er tour
            self.select_a_new_destination()
            self.state = 1
            next_position = self.next_move()
        elif self.state == 1:
            if pos == self.destination:
                self.state = 2
                next_position = self.next_move()
            else:
                next_position = self.compute_next_position()
                if not self.board.cell_available(next_position):
                    # prochaine cellule deja prise
                    neighboors = self.board.get_neighboors_available(pos)
                    # print >> sys.stderr, "neighboors: ", neighboors
                    if neighboors:
                        distances_neighboors_to_destination = map(
                            lambda neighboor: self.board.distance(neighboor, self.destination),
                            neighboors
                        )
                        next_position = min(
                            zip(distances_neighboors_to_destination, neighboors),
                            key=lambda tup: tup[0]
                        )[1]
                    elif not self.board.cell_available(self.destination):
                        self.select_a_new_destination()
                        next_position = self.next_move()
                        # sinon on continue vers la destination
        elif self.state == 2:
            # on est arrive a la bordure, on cherche a fermer le rectangle
            rect = self.cur_rect
            # on recupere les voisins libres autour de la cellule bordure atteinte
            neighboors_available = self.board.get_neighboors_available(pos)
            # on filtre les voisins libres pour recuperer les voisins sur la bordure du rectangle
            neighboors_on_rect_borders = filter(lambda pos: rect.isOnBorder(pos[::-1]), neighboors_available)
            # Est ce qu'on a acces a une bordure ?
            if neighboors_on_rect_borders:
                print >> sys.stderr, "sur la bordure"
                # si oui, on s'y dirige (normalement 1 disponible ... mais a verifier)
                next_position = neighboors_on_rect_borders.pop()
            else:
                print >> sys.stderr, "DECROCHAGE de la bordure"
                # sinon on a un soucy d'accessibilite
                # on decide d'aller chercher un nouveau rectangle libre [WIP]
                self.state = 0
                next_position = self.next_move()

        return next_position

    def select_a_new_rect(self):
        """ """
        # Translates input into a list of coordinates of free elements
        freeElements = [(pos[1], pos[0]) for pos in self.board.get_cells_available()]
        # freeElements = self.board.get_cells_available_or_possessed_by_id('0')

        # Find and print open rectangles
        openRects = findOpenRectangles(freeElements, self.board.h)
        #for openRect in openRects:
        #    print >> sys.stderr, openRect

        # on determine le rectangle 'libre' d'aire max
        rect_with_max_area = max(openRects, key=lambda rect: rect.area())

        return rect_with_max_area

    def select_a_new_destination(self):
        """ """
        #
        rect_choosen = self.select_a_new_rect()
        self.cur_rect = rect_choosen

        # on recupere le centre du rectangle d'aire max
        # center_rect_with_max_area = rect_choosen.center()
        #print >> sys.stderr, "center_rect_with_max_area: ", center_rect_with_max_area
        # on choisit le centre du rectangle d'aire max comme destination
        #self.destination = (center_rect_with_max_area[1], center_rect_with_max_area[0])

        # A* : Path finding
        #came_from, cost_so_far = a_star_search(self.board, self.me.position, center_rect_with_max_area)
        #path = reconstruct_path(came_from, start=self.me.position, goal=center_rect_with_max_area)
        #print >> sys.stderr, "path :", path

        # on cherche le bord 'accessible' (le plus proche) du rectangle choisit
        self.destination = self.board.compute_nearest_position_on_border_for_rect(self.me.position, rect_choosen)

        print >> sys.stderr, "rect_choosen: ", rect_choosen
        print >> sys.stderr, "self.destination: ", self.destination

        return self.destination

    def compute_next_position(self):
        """ """
        pos = self.me.position
        dst = self.destination
        # => priorite deplacement en abscisse (x)
        if pos[0] != dst[0]:
            return pos[0] + (1 if pos[0] < dst[0] else -1), pos[1]
        else:  # puis en ordonnee (y)
            return pos[0], pos[1] + (1 if pos[1] < dst[1] else -1)

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

opponent_count = int(raw_input())  # Opponent count

game = GameStrategy(opponent_count)

# game loop
while 1:
    game_round = int(raw_input())
    game.update_game_round(game_round)

    # x: Your x position
    # y: Your y position
    # back_in_time_left: Remaining back in time
    x, y, back_in_time_left = [int(i) for i in raw_input().split()]
    game.update_me(x, y, back_in_time_left)

    for i in xrange(opponent_count):
        # opponent_x: X position of the opponent
        # opponent_y: Y position of the opponent
        # opponent_back_in_time_left: Remaining back in time of the opponent
        opponent_x, opponent_y, opponent_back_in_time_left = [int(j) for j in raw_input().split()]
        game.update_opponent(i, opponent_x, opponent_y, opponent_back_in_time_left)

    for i in xrange(20):
        line = raw_input()  # One line of the map ('.' = free, '0' = you, otherwise the id of the opponent)
        game.update_board(i, line)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # action: "x y" to move or "BACK rounds" to go back in time
    # print "17 10"
    print game.format_output(game.next_move())