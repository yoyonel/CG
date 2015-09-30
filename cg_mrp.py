import sys
import math
import random


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
        return (self.end + self.start)//2

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

    #def intersect(self, other):
    #    return Range(max(self.start, other.start), min(self.end, other.end))

    def contains(self, other):
        return self.xRange.contains(other.xRange) and self.yRange.contains(other.yRange)

    def area(self):
        """ """
        return self.xRange.len() * self.yRange.len()

    def center(self):
        """ """
        return self.xRange.center(), self.yRange.center()

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
    #for freeRuns in freeRunsPerRow.items():
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


class Board:
    """ """
    cardinals = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    #cardinals = [(x, y) for y in xrange(-1, 2) for x in xrange(-1, 2) if bool(x) | bool(y)]

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

        if pos == self.destination:
            self.select_a_new_destination()
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

        return next_position

    def select_a_new_destination(self):
        """ """
        # Translates input into a list of coordinates of free elements
        freeElements = [(pos[1], pos[0]) for pos in self.board.get_cells_available()]
        #freeElements = self.board.get_cells_available_or_possessed_by_id('0')
        # Find and print open rectangles
        openRects = findOpenRectangles(freeElements, self.board.h)
        #for openRect in openRects:
        #    print >> sys.stderr, openRect
        rect_with_max_area = max(openRects, key=lambda rect: rect.area())
        center_rect_with_max_area = rect_with_max_area.center()
        print >> sys.stderr, "center_rect_with_max_area: ", center_rect_with_max_area
        
        self.destination = (center_rect_with_max_area[1], center_rect_with_max_area[0])

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
