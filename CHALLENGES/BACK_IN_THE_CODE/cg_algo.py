import sys
import math


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
    def __init__(self, _l=35, _h=20):
        """ """
        self.l = _l
        self.h = _h
        self.center = (_l//2, _h//2)
        self.board = ['.' * _l] * _h

    def update(self, _i_line, _line):
        """ """
        self.board[_i_line] = _line

    def distance(self, _pos0, _pos1):
        """
         Manhattan distance
        """
        return abs(_pos1[0] - _pos0[0]) + abs(_pos1[1] - _pos0[1])

    def projections_to_borders(self, _pos):
        """ """
        return [
            (0, _pos[1]),            # WEST BORDER
            (self.l-1, _pos[1]),     # EAST BORDER
            (_pos[0], 0),            # NORTH BORDER
            (_pos[0], self.h-1),     # SOUTH BORDER
        ]

    def distances_to_borders(self, _pos):
        """ """
        l_pos = [_pos]*4
        proj_to_borders = self.projections_to_borders(_pos)
        return zip(map(lambda tup: self.distance(tup[0], tup[1]), zip(proj_to_borders, l_pos)), proj_to_borders)

    def get_border_from_direction(self, _str_direction):
        """ """
        if _str_direction == 'NORTH':
            return Border(0, Border.Type.HORIZONTAL)
        elif _str_direction == 'SOUTH':
            return Border(self.h-1, Border.Type.HORIZONTAL)
        elif _str_direction == 'WEST':
            return Border(0, Border.Type.VERTICAL)
        else:
            return Border(self.l-1, Border.Type.VERTICAL)


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
        #
        self.destination = self.board.center
        #
        self.state = 0
        #
        self.indice_cycle_direction = 0
        self.borders_to_reach = []

    def next_move(self):
        """ """
        next_destination = [0, 0]

        if self.state == 0:
            # 1er tour => init
            self.compute_borders()
            next_destination = self.compute_destination()
            self.destination = next_destination
            self.state = 1
        elif self.state == 1:
            pos = self.me.position
            if pos == self.destination:
                self.compute_borders_from_center()
                next_destination = self.compute_destination()
                self.destination = next_destination
                self.state = 2
            else:
                next_destination = self.compute_destination()

        return self.format_output(next_destination)

    def get_border_from_rotation_cycle(self):
        """
        :return:
        """
        return self.board.get_border_from_direction(self.CycleDirections[self.indice_cycle_direction])

    def next_rotation_cycle(self):
        """
        :return:
        """
        self.indice_cycle_direction = (self.indice_cycle_direction+1) % 4
        return self.indice_cycle_direction

    @staticmethod
    def format_output(_destination):
        """
        :return:
        """
        return "%d %d" % (_destination[0], _destination[1])

    def compute_borders_from_center(self):
        """
        :param _obj_pos:
        """
        pos = self.board.center
        #
        self.borders_to_reach.append(self.get_border_from_rotation_cycle())
        self.next_rotation_cycle()
        self.borders_to_reach.append(self.get_border_from_rotation_cycle())
        self.next_rotation_cycle()
        self.borders_to_reach.append(Border(pos[0], Border.Type.HORIZONTAL))
        self.borders_to_reach.append(Border(pos[1], Border.Type.VERTICAL))
        print >> sys.stderr, "self.borders_to_reach:", self.borders_to_reach

    def compute_borders(self):
        """
         Calcul des bords au depart [INIT]
        """
        for _ in xrange(4):
            self.borders_to_reach.append(self.get_border_from_rotation_cycle())
            self.next_rotation_cycle()
        #print >> sys.stderr, "self.borders_to_reach:", self.borders_to_reach

    def compute_destination(self):
        """
        :param _obj_pos:
        :return:
        """
        #
        print >> sys.stderr, "self.borders_to_reach:", self.borders_to_reach
        destination = self.me.position
        if len(self.borders_to_reach):
            pos = self.me.position
            l_pos = [pos] * len(self.borders_to_reach)
            # distance des bords (filter des distances nulles)
            tup_distances_to_borders = zip(
                map(lambda tup: tup[0].distance(tup[1]), zip(self.borders_to_reach, l_pos)),
                l_pos
            )
            tup_distances_to_borders = filter(lambda tup: tup[0], tup_distances_to_borders)
            # min distance to border
            tup_min_distance_to_border = min(tup_distances_to_borders, key=lambda tup: tup[0])
            #min_distance_to_border = tup_min_distance_to_border[0]
            destination = tup_min_distance_to_border[1]

            print >> sys.stderr, "destination:", destination

        return destination

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
    #print "17 10"
    print game.next_move()
