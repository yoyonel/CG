import sys
from itertools import groupby
from collections import defaultdict
import copy


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
        #
        self.gb_on_ca = None

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
            _row, _col, i_round_for_explosion = tup_bomb
            if i_round_for_explosion >= self.rounds:
                self.do_explosion(_row, _col)

    def do_explosion(self, _i_row, _i_col):
        """

        :param _i_row:
        :param _i_col:
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

        :param _i_row:
        :param _i_col:
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
        self.map_max_connectivities = defaultdict(list)
        #
        self.list_available_cells = []

    def reset_map_action_bombs(self):
        """

        :return:
        """
        self.map_action_bombs = [[0] * width for _ in xrange(height)]
        self.map_max_connectivities = defaultdict(list)

    def update_influences_of_nodes(self):
        """

        :return:
        """
        for i_row, row_tiles in enumerate(self.rows_tiles):
            for i_col, tile in enumerate(row_tiles):
                if tile == self.t_tiles['TILE_NODE']:
                    self.compute_influences_of_nodes(i_row, i_col)

    def compute_max_connectivity_for_cell(self, tag_cell):
        """

        :param tag_cell:
        :return:
        """
        map_max_connectivities = defaultdict(list)
        for i_row, row_tiles in enumerate(self.rows_tiles):
            for i_col, tile in enumerate(row_tiles):
                if tile == tag_cell:
                    max_connectivity = self.compute_max_connectivity_for_node(i_row, i_col)
                    map_max_connectivities[max_connectivity].append((i_row, i_col))
        return map_max_connectivities

    def update_max_connectivity_for_nodes(self):
        """

        :return:
        """
        self.map_max_connectivities = self.compute_max_connectivity_for_cell(self.t_tiles['TILE_NODE'])

    def compute_max_connectivity_for_nodes_T(self):
        """

        :return:
        """
        return self.compute_max_connectivity_for_cell('T')

    def compute_influences_of_nodes(self, _i_row, _i_col):
        """

        :param _i_row:
        :param _i_col:
        :return:
        """
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_col + offset) < self.l):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                # if self.rows_tiles[_i_row][_i_col + offset] is self.t_tiles['TILE_EMPTY']:
                self.map_action_bombs[_i_row][_i_col + offset] += 1
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_col + offset) > -1):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                # if self.rows_tiles[_i_row][_i_col + offset] is self.t_tiles['TILE_EMPTY']:
                self.map_action_bombs[_i_row][_i_col + offset] += 1
            else:
                break
            offset -= 1
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_row + offset) < self.h):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                # if self.rows_tiles[_i_row + offset][_i_col] is self.t_tiles['TILE_EMPTY']:
                self.map_action_bombs[_i_row + offset][_i_col] += 1
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_row + offset) > -1):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                # if self.rows_tiles[_i_row + offset][_i_col] is self.t_tiles['TILE_EMPTY']:
                self.map_action_bombs[_i_row + offset][_i_col] += 1
            else:
                break
            offset -= 1

    def compute_max_connectivity_for_node(self, _i_row, _i_col):
        """

        :param _i_row:
        :param _i_col:
        :return:
        """
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        max_value = 0
        while (offset < 4) & ((_i_col + offset) < self.l):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                max_value = max(max_value, self.map_action_bombs[_i_row][_i_col + offset])
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_col + offset) > -1):
            if self.rows_tiles[_i_row][_i_col + offset] is not self.t_tiles['TILE_WALL']:
                max_value = max(max_value, self.map_action_bombs[_i_row][_i_col + offset])
            else:
                break
            offset -= 1
        # propagation de l'action de la bombe en horizontal positif
        offset = 1
        while (offset < 4) & ((_i_row + offset) < self.h):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                max_value = max(max_value, self.map_action_bombs[_i_row + offset][_i_col])
            else:
                break
            offset += 1
        # propagation de l'action de la bombe en horizontal negatif
        offset = -1
        while (offset > -4) & ((_i_row + offset) > -1):
            if self.rows_tiles[_i_row + offset][_i_col] is not self.t_tiles['TILE_WALL']:
                max_value = max(max_value, self.map_action_bombs[_i_row + offset][_i_col])
            else:
                break
            offset -= 1
        #
        return max_value

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

    def update_gb_ca_connectivity(self):
        """

        :return:
        """
        self.gb_on_ca = groupby(self.list_available_cells, lambda tup: tup[2])  # groupby on value

    def __copy__(self):
        """
        :return:
        """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __repr__(self):
        """
        :return:
        """
        return \
            '\n'.join(map(str, self.rows_tiles)) + '\n' + \
            '\n'.join([reduce(lambda a, b: str(a) + ' ' + str(b), _row) for _row in self.map_action_bombs]) + '\n' + \
            ', '.join(map(str, self.list_available_cells))


def compute_gb_connectivity(l):
    """

    :param l:
    :return:
    """
    l_c = defaultdict(list)
    for _row, _col, value in l:
        l_c[value].append((_row, _col))
    return l_c


def compute_best_position_for_bomb(solver):
    """

    :param solver:
    :return:
    """
    # ###################################################################################
    # strategie 2:
    # ###################################################################################
    print >> sys.stderr, "Solver [avant]:\n", solver

    list_connectivities = compute_gb_connectivity(solver.list_available_cells)
    list_values = sorted(list_connectivities.keys(), reverse=True)
    print >> sys.stderr, "list_values: ", list_values

    solver.update_max_connectivity_for_nodes()
    print >> sys.stderr, "solver.map_max_connectivities (avant explosion): ", solver.map_max_connectivities
    nb_ca_with_c1_before_explosion = len(solver.map_max_connectivities[1])
    print >> sys.stderr, "nombre de ca avec connectivite 1 (avant explosion): ", nb_ca_with_c1_before_explosion

    # print >> sys.stderr, "list_values: ", list_values
    _row, _col = 0, 0
    nb_ca_with_c1_after_explosion = nb_ca_with_c1_before_explosion + 1
    value = 0
    for value in list_values:
        for _row, _col in list_connectivities[value]:
            # on recupere la position de cellule libre la plus rentable en terme d'explosion
            print >> sys.stderr, "value: %d -> coord cell: (%d, %d): " % (value, _row, _col)

            # On cree une copie du solver pour effectuer un test de validite du prochain mouvement
            solver_2 = copy.deepcopy(solver)
            print >> sys.stderr, "%s %s" % (hex(id(solver)), hex(id(solver_2)))
            solver_2.set_bomb_fork(_row, _col)
            solver_2.update_max_connectivity_for_nodes()
            #nb_ca_with_c1_after_explosion = len(filter(lambda v: v == 1, solver_2.map_max_connectivity.values()))
            nb_ca_with_c1_after_explosion = len(solver_2.map_max_connectivities[1])
            print >> sys.stderr, "nombre de ca avec connectivite 1 (apres explosion): ", nb_ca_with_c1_after_explosion
            if nb_ca_with_c1_after_explosion <= nb_ca_with_c1_before_explosion:
                break
        print >> sys.stderr, ""
        if nb_ca_with_c1_after_explosion <= nb_ca_with_c1_before_explosion:
            break

    return _row, _col, value


def compute_next_move(solver, _state):
    """

    :param solver:
    :return:
    """
    if _state == 0:
        if bool(solver.bombs) & bool(solver.list_available_cells):
            # calcul de la 'meilleur' position pour placer une bombe au prochain tour
            _row, _col, value = compute_best_position_for_bomb(solver)
            print >> sys.stderr, "row, col, value: ", _row, _col, value

            if solver.bombs == 1:
                # il ne reste qu'une bombe
                # on test pour voir si en attendant on a pas un meilleur coup possible
                solver_2 = copy.deepcopy(solver)
                solver_2.update(rounds - 3, bombs)
                solver_2.update_list_cells_availables()
                row2, col2, value2 = compute_best_position_for_bomb(solver_2)
                print >> sys.stderr, "row2, col2, value2: ", row2, col2, value2
                if value2 > value:
                    return (row2, col2), 1

            solver.set_bomb_fork(_row, _col)

            return (_row, _col), 0
        else:
            return 'WAIT', 0
    elif _state == 1:
        return 'WAIT', 1


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

state = 0
# game loop
while 1:
    # rounds: number of rounds left before the end of the game
    # bombs: number of bombs left
    rounds, bombs = [int(i) for i in raw_input().split()]
    grid.update(rounds, bombs)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # next_action = grid.next_action()
    next_action, state = compute_next_move(grid, state)
    print >> sys.stderr, "next_action, state: ", next_action, state

    if next_action == 'WAIT':
        print 'WAIT'
    elif state == 1:
        row, col = next_action
        print >> sys.stderr, "grid.rows_tiles[row][col]: ", grid.rows_tiles[row][col]
        while grid.rows_tiles[row][col] == 'T':
            print 'WAIT'
            rounds, bombs = [int(i) for i in raw_input().split()]
            grid.update(rounds, bombs)
        print "%d %d" % (col, row)
        state = 0
    else:
        print "%d %d" % (next_action[1], next_action[0])
