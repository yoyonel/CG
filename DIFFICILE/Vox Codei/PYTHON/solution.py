import sys


class GridForVoxCodei(object):
    """

    """
    t_tiles = dict(
        frozenset(
            {
                'TILE_WALL': '#',
                'TILE_NODE': '@',
                'TILE_EMPTY': '.'
            }.items()
        )
    )

    def __init__(self, _l, _h):
        """

        :param _l:
        :param _h:
        :return:
        """
        self.l = _l
        self.h = _h
        #
        self.bombs = -1
        self.rounds = -1
        #
        self.rows_tiles = []
        #
        self.list_bombs = []

    def append_row(self, _row_tiles):
        """

        :param _row_tiles:
        :return:
        """
        self.rows_tiles.append(list(_row_tiles))

    def update(self, _rounds, _bombs):
        """

        :param _rounds:
        :param _bombs:
        :return:
        """
        #
        self.rounds = _rounds
        self.bombs = _bombs
        #
        for tup_bomb in self.list_bombs:
            row, col, i_round_for_explosion = tup_bomb
            if i_round_for_explosion == self.rounds:
                self.do_explosion(row, col)

    def do_explosion(self, _i_row, _i_col):
        """

        :param _action:
        :return:
        """
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_col + offset) < self.l):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                self.rows_tiles[_i_row][_i_col + offset] = self.t_tiles['TILE_EMPTY']
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_col + offset) > -1):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                self.rows_tiles[_i_row][_i_col + offset] = self.t_tiles['TILE_EMPTY']
            else:
                break
            offset -= 1
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_row + offset) < self.h):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                self.rows_tiles[_i_row + offset][_i_col] = self.t_tiles['TILE_EMPTY']
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_row + offset) > -1):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                self.rows_tiles[_i_row + offset][_i_col] = self.t_tiles['TILE_EMPTY']
            else:
                break
            offset -= 1
        #
        self.rows_tiles[_i_row][_i_col] = self.t_tiles['TILE_EMPTY']

    def prepare_explosion(self, _i_row, _i_col):
        """

        :param _action:
        :return:
        """
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_col + offset) < self.l):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row][_i_col + offset] == self.t_tiles['TILE_NODE']:
                    self.rows_tiles[_i_row][_i_col + offset] = 'T'
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_col + offset) > -1):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row][_i_col + offset] == self.t_tiles['TILE_NODE']:
                    self.rows_tiles[_i_row][_i_col + offset] = 'T'
            else:
                break
            offset -= 1
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_row + offset) < self.h):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row + offset][_i_col] == self.t_tiles['TILE_NODE']:
                    self.rows_tiles[_i_row + offset][_i_col] = 'T'
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_row + offset) > -1):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row + offset][_i_col] == self.t_tiles['TILE_NODE']:
                    self.rows_tiles[_i_row + offset][_i_col] = 'T'
            else:
                break
            offset -= 1

    def unprepare_explosion(self, _i_row, _i_col):
        """

        :param _action:
        :return:
        """
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_col + offset) < self.l):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row][_i_col + offset] == 'T':
                    self.rows_tiles[_i_row][_i_col + offset] = self.t_tiles['TILE_NODE']
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_col + offset) > -1):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row][_i_col + offset] == 'T':
                    self.rows_tiles[_i_row][_i_col + offset] = self.t_tiles['TILE_NODE']
            else:
                break
            offset -= 1
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_row + offset) < self.h):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row + offset][_i_col] == 'T':
                    self.rows_tiles[_i_row + offset][_i_col] = self.t_tiles['TILE_NODE']
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_row + offset) > -1):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row + offset][_i_col] == 'T':
                    self.rows_tiles[_i_row + offset][_i_col] = self.t_tiles['TILE_NODE']
            else:
                break
            offset -= 1


class SolverForVoxCodei(GridForVoxCodei):
    """

    """
    t_tiles = dict(
        frozenset(
            {
                'TILE_WALL': '#',
                'TILE_NODE': '@',
                'TILE_EMPTY': '.'
            }.items()
        )
    )

    def __init__(self, _l, _h):
        """

        :param _l:
        :param _h:
        :return:
        """
        super(SolverForVoxCodei, self).__init__(_l, _h)

        self.map_action_bombs = [[0] * width for _ in xrange(height)]
        #
        self.list_available_cells = []

    def reset_map_action_bombs(self):
        """

        :return:
        """
        self.map_action_bombs = [[0] * width for _ in xrange(height)]

    def update_influences_of_nodes(self):
        """

        :return:
        """
        for i_row, row_tiles in enumerate(self.rows_tiles):
            for i_col, tile in enumerate(row_tiles):
                if tile == self.t_tiles['TILE_NODE']:
                    self.compute_influences_of_nodes(i_row, i_col)

    def compute_influences_of_nodes(self, _i_row, _i_col):
        """

        :param _action:
        :return:
        """
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_col + offset) < self.l):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row][_i_col + offset] is self.t_tiles['TILE_EMPTY']:
                    self.map_action_bombs[_i_row][_i_col + offset] += 1
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_col + offset) > -1):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row][_i_col + offset] is self.t_tiles['TILE_EMPTY']:
                    self.map_action_bombs[_i_row][_i_col + offset] += 1
            else:
                break
            offset -= 1
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_row + offset) < self.h):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row + offset][_i_col] is self.t_tiles['TILE_EMPTY']:
                    self.map_action_bombs[_i_row + offset][_i_col] += 1
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_row + offset) > -1):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                if self.rows_tiles[_i_row + offset][_i_col] is self.t_tiles['TILE_EMPTY']:
                    self.map_action_bombs[_i_row + offset][_i_col] += 1
            else:
                break
            offset -= 1

    def update_list_cells_availables(self):
        """

        :return:
        """
        self.list_available_cells = [
            (i_row, i_col, self.map_action_bombs[i_row][i_col])
            for i_row, row_tiles in enumerate(self.rows_tiles)
            for i_col, tile in enumerate(row_tiles)
            if tile is self.t_tiles['TILE_EMPTY']
        ]

    def sort_list_ac_key_0(self):
        """

        :return:
        """
        #
        self.list_available_cells.sort(key=lambda tup_coords: self.map_action_bombs[tup_coords[0]][tup_coords[1]])

    def apply_fork(self, _i_row, _i_col):
        """

        :param _i_row:
        :param _i_col:
        :return:
        """
        self.do_explosion(_i_row, _i_col)
        self.update_influences_of_nodes()
        self.update_list_cells_availables()

    def set_bomb_fork(self, _i_row, _i_col):
        """

        :param _i_row:
        :param _i_col:
        :return:
        """
        self.rows_tiles[_i_row][_i_col] = 'B'
        self.prepare_explosion(_i_row, _i_col)
        self.reset_map_action_bombs()
        self.update_influences_of_nodes()
        self.update_list_cells_availables()
        self.list_bombs.append((_i_row, _i_col, max(0, self.rounds - 3)))

    def unset_bomb_fork(self, _i_row, _i_col):
        """

        :param _i_row:
        :param _i_col:
        :return:
        """
        self.rows_tiles[_i_row][_i_col] = self.t_tiles['TILE_EMPTY']
        self.unprepare_explosion(_i_row, _i_col)
        self.reset_map_action_bombs()
        self.update_influences_of_nodes()
        self.update_list_cells_availables()
        self.list_bombs.pop()

    def count_ca_to_0connectivity(self):
        """

        :return:
        """
        return len(
            [
                0
                for tup_coords in self.list_available_cells
                if (not self.map_action_bombs[tup_coords[0]][tup_coords[1]])
            ]
        )

    def next_action(self):
        """

        :return:
        """
        if bool(self.bombs) & bool(self.list_available_cells):
            # ###################################################################################
            # strategie 0: naive, on choisit l'emplacement libre qui detruit le plus de noeuds
            # ###################################################################################
            '''
            self.sort_list_ac_key_0()
            row, col = self.list_available_cells.pop(-1)
            self.set_bomb_fork(row, col)
            return row, col
            '''
            # ###################################################################################

            ####################################################################################
            # strategie 1: pareil que 0 mais on verifie qu'on elimine au moins "un groupe"
            ####################################################################################
            ca_0c_before_explosion = self.count_ca_to_0connectivity()
            print >> sys.stderr, "ca_0c_before_explosion: ", ca_0c_before_explosion
            self.sort_list_ac_key_0()
            row, col = 0, 0
            while self.list_available_cells:
                row, col, value = self.list_available_cells.pop(-1)
                print >> sys.stderr, "row, col, value: ", row, col, value
                self.set_bomb_fork(row, col)
                ca_0c_after_explosion = self.count_ca_to_0connectivity()
                print >> sys.stderr, "ca_0c_after_explosion: ", ca_0c_after_explosion

                if ca_0c_after_explosion is not ca_0c_before_explosion:
                    break
                self.unset_bomb_fork(row, col)
            self.set_bomb_fork(row, col)
            return row, col
            ####################################################################################

        else:
            return 'WAIT'

    def __repr__(self):
        """
        :return:
        """
        return \
            '\n'.join(map(str, self.rows_tiles)) + '\n' + \
            '\n'.join([reduce(lambda a, b: str(a) + ' ' + str(b), row) for row in self.map_action_bombs]) + '\n' + \
            ', '.join(map(str, self.list_available_cells))

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# width: width of the firewall grid
# height: height of the firewall grid
width, height = [int(i) for i in raw_input().split()]
grid = SolverForVoxCodei(width, height)

for i in xrange(height):
    map_row = raw_input()  # one line of the firewall grid
    grid.append_row(map_row)

grid.update_influences_of_nodes()
grid.update_list_cells_availables()
print >> sys.stderr, "grid:\n", grid

# game loop
while 1:
    # rounds: number of rounds left before the end of the game
    # bombs: number of bombs left
    rounds, bombs = [int(i) for i in raw_input().split()]
    grid.update(rounds, bombs)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # print "3 0"
    next_action = grid.next_action()
    if next_action == 'WAIT':
        print 'WAIT'
    else:
        print "%d %d" % (next_action[1], next_action[0])
    print >> sys.stderr, "grid:\n", grid
