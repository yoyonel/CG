import math
import operator
import sys
from collections import defaultdict


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
        """ """
        return Range(max(self.start, other.start), min(self.end, other.end))

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def len(self):
        """ """
        return self.end - self.start

    def center(self):
        """ """
        return (self.end + self.start) / 2.0

    def clamp(self, value):
        """ """
        return max(min(value, self.end), self.start)

    def inside(self, value):
        """

        :param value:
        :return:
        """
        return self.start <= value <= self.end

    def __repr__(self):
        return "Range(%s,%s)" % (self.start, self.end)


class SolverWithAACut:
    #
    # def __init__(self, _w, _h, _x, _y, _bomb_dist='UNKNOWN'):
    def __init__(self, _wc_grid_dimensions, _wc_initial_batman_position, _bomb_dist='UNKNOWN'):
        """

        :param _wc_grid_dimensions: windows coordinates -> dimension de la grille
        :param _wc_initial_batman_position: wc -> position initiale de batman
        :param _bomb_dist: etat initial (surement egale a 'UNKNOWN') de Batman par rapport a la bombe
        :return:
        """
        #
        width_grid, height_grid = _wc_grid_dimensions
        self.wc_xRange = Range(0, width_grid - 1)
        self.wc_yRange = Range(0, height_grid - 1)
        #
        self.wc_initial_dimensions = (self.wc_xRange, self.wc_yRange)
        # position courante du batman [Windows_Coordinates]
        self.wc_position = _wc_initial_batman_position
        # derniere position du batman (windows coordinates)
        self.wc_last_position = self.wc_position
        #
        self.bomb_dist = _bomb_dist
        # ac : analytic coordinates [Analytic_Coordinates]
        self.ac_cut_position = 0
        self.type_cut = ''

    def update_ranges(self, _bomb_dist):
        """

        :param _bomb_dist:
        :return:
        """

        if _bomb_dist == 'SAME':
            # cut_position forcement sur une cellule
            # print >> sys.stderr, "SAME -> self.ac_cut_position: ", self.ac_cut_position
            #assert self.position_on_cell(self.ac_cut_position)
            if self.type_cut == 'VERTICAL':
                # une seule colonne nous interesse
                self.wc_xRange = Range(self.ac_cut_position, self.ac_cut_position)
            elif self.type_cut == 'HORIZONTAL':
                # une seule ligne nous interesse
                self.wc_yRange = Range(self.ac_cut_position, self.ac_cut_position)
                # on passe en recherche unidimensionnelle 1D
        else:
            offset = 0.5 * (1 + self.position_on_cell(self.ac_cut_position))
            if _bomb_dist == 'WARMER':
                if self.type_cut == 'VERTICAL':
                    if self.wc_position[0] > self.ac_cut_position:
                        self.wc_xRange.start = self.ac_cut_position + offset
                    else:
                        self.wc_xRange.end = self.ac_cut_position - offset
                elif self.type_cut == 'HORIZONTAL':
                    if self.wc_position[1] > self.ac_cut_position:
                        self.wc_yRange.start = self.ac_cut_position + offset
                    else:
                        self.wc_yRange.end = self.ac_cut_position - offset
            elif _bomb_dist == 'COLDER':
                if self.type_cut == 'VERTICAL':
                    if self.wc_last_position[0] > self.ac_cut_position:
                        self.wc_xRange.start = self.ac_cut_position + offset
                    else:
                        self.wc_xRange.end = self.ac_cut_position - offset
                elif self.type_cut == 'HORIZONTAL':
                    if self.wc_last_position[1] > self.ac_cut_position:
                        self.wc_yRange.start = self.ac_cut_position + offset
                    else:
                        self.wc_yRange.end = self.ac_cut_position - offset
                        # else _bomb_dist == 'UNKNOWN' => rien a faire

    @staticmethod
    def position_on_cell(_position):
        """

        :param _position:
        :return:
        """
        # return _position != int(_position)
        return _position == int(_position)

    @staticmethod
    def compute_central_symmetry(position, center):
        """

        :param position:
        :param center:
        :return:
        """
        return 2.0 * center - position

    @staticmethod
    def anch_to_grid(_position):
        """

        :param _position:
        :return:
        """
        return int(_position) + round(_position % 1) * 0.5

    @staticmethod
    def anch_to_cell(_position, _range):
        """

        :param _position:
        :param _range:
        :return:
        """
        position_on_cell = _range.clamp(_position)
        if not SolverWithAACut.position_on_cell(_position):
            position_on_cell = SolverWithAACut.anch_to_grid(_position)
            if _range.inside(position_on_cell + 0.5):
                position_on_cell += 0.5
            elif _range.inside(position_on_cell - 0.5):
                position_on_cell -= 0.5
        return position_on_cell

    @staticmethod
    def compute_range_centers(_position, _range, _init_range):
        """

        :param _range:
        :param _position:
        :param _init_range:
        :return:
        """
        #
        center_start = _range.start if _position < _range.start else _init_range.start
        center_end = _init_range.end
        # calcul du centre de l'intervalle
        center_start = (_position + center_start) * 0.5
        center_end = (_position + center_end) * 0.5
        # 'accrochage' a la grille
        center_start = SolverWithAACut.anch_to_grid(center_start)
        center_end = SolverWithAACut.anch_to_grid(center_end)
        # construction de l'intervalle des positions des centres
        range_centers = Range(center_start, center_end)
        range_centers = range_centers.intersect(_range)
        # on s'assure que de ne pas avoir un centre sur la position
        range_centers.start += 0.5 * (range_centers.start == _position)
        range_centers.end -= 0.5 * (range_centers.end == _position)
        # on renvoie l'intervalle resultat
        return () if range_centers.isEmpty() else range_centers

    def compute_cut(self, _position, _range, _init_range):
        """
        :param _range:
        :return:
        """
        range_centers = self.compute_range_centers(_position, _range, _init_range)
        ac_center = _range.center()
        if range_centers:
            # des centres sont addressables
            # centre qu'on cherche a atteindre
            if not range_centers.inside(ac_center):
                # on ne peut pas atteindre ce centre
                # on clamp la valeur du centre avec la plus proche dans l'intervalle
                ac_center = range_centers.clamp(ac_center)
                # on tente de positionner le centre sur une cellule (pour optimiser le 'SAME' result)
                ac_center = self.anch_to_cell(ac_center, range_centers)
            #
            ac_center = _range.clamp(self.anch_to_grid(ac_center))

        ac_cs = self.compute_central_symmetry(_position, ac_center)
        wc_cs = self.anch_to_cell(ac_cs, _init_range)
        if wc_cs == _position:
            print >> sys.stderr, "wc_cs == _last_pos"
            # on ne peut pas ne pas se deplacer
            if wc_cs == _init_range.end:
                wc_cs -= 1
            else:
                wc_cs += 1
        ac_center = (_position + wc_cs) * 0.5

        return wc_cs, ac_center

    def compute_vertical_cut(self):
        """

        :return:
        """
        return self.compute_cut(self.wc_position[0], self.wc_xRange, self.wc_initial_dimensions[0])

    def compute_horizontal_cut(self):
        """

        :return:
        """
        return self.compute_cut(self.wc_position[1], self.wc_yRange, self.wc_initial_dimensions[1])

    @staticmethod
    def eval_split(_position, _range):
        """

        :param _position:
        :param _range:
        :return:
        """
        coef_split = 0.0
        if _range.inside(_position):
            coef_split = min(abs(_range.start - _position), abs(_range.end - _position))

        return coef_split

    def compute_next_position(self, _bomb_dist):
        """

        :return:
        """
        self.bomb_dist = _bomb_dist

        # maj des ranges par rapport a la reponse du scanner de Batman
        self.update_ranges(_bomb_dist)

        print >> sys.stderr, "-> ", self.wc_xRange.isUnit(), self.wc_yRange.isUnit()
        # est ce que les ranges sont reduites a l'unite ?
        if self.wc_xRange.isUnit() & self.wc_yRange.isUnit():
            print >> sys.stderr, "UNITES pour les ranges!"
            # si oui, on a la solution du probleme
            next_position = (self.wc_xRange.start, self.wc_yRange.start)
        else:

            wc_cs_h, ac_center_h = self.compute_horizontal_cut()
            eval_h = self.eval_split(ac_center_h, self.wc_yRange)
            # print >> sys.stderr, "wc_cs_h:%s\nac_center_h:%s\neval_h:%s\nself.wc_yRange:%s\n" % (
            #    wc_cs_h, ac_center_h, eval_h, self.wc_yRange)

            wc_cs_v, ac_center_v = self.compute_vertical_cut()
            eval_v = self.eval_split(ac_center_v, self.wc_xRange)
            #print >> sys.stderr, "wc_cs_v:%s\nac_center_v:%s\neval_v:%s\nself.wc_yRange:%s\n" % (
            #    wc_cs_v, ac_center_v, eval_v, self.wc_yRange)

            # cut VERTICAL ou HORIZONTAL a evaluations nulles
            # on se repositionne (vers le centre) a defaut de couper dans le vent !
            if (eval_h == 0) & (eval_v == 0):
                type_cut = 'NO_CUT'
                # TODO: on galere avec les coordonnees sur le centre, faudrait resoudre ce cas ...
                next_position = (
                    self.anch_to_cell(self.wc_xRange.center() + 1, self.wc_initial_dimensions[0]),
                    self.anch_to_cell(self.wc_yRange.center() + 1, self.wc_initial_dimensions[1])
                )
                cut_position = 0
            elif eval_v > eval_h:
                type_cut = 'VERTICAL'
                next_position = (wc_cs_v, self.wc_position[1])
                cut_position = ac_center_v
            else:
                type_cut = 'HORIZONTAL'
                next_position = (self.wc_position[0], wc_cs_h)
                cut_position = ac_center_h

            self.wc_last_position = self.wc_position
            self.wc_position = next_position
            self.ac_cut_position = cut_position
            self.type_cut = type_cut

        return next_position

    # String representaion (for debugging)
    def __repr__(self):
        return '[WC] Ranges: %s - %s\n[WC] last_position: %s\n[WC] position: %s\n' \
               '[AC] cut_position: %s\ntype_cut: %s\nbomb_dist: %s\n' % (
                   self.wc_xRange, self.wc_yRange,
                   self.wc_last_position,
                   self.wc_position,
                   self.ac_cut_position,
                   self.type_cut,
                   self.bomb_dist
        )

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.


w, h = [int(i) for i in raw_input().split()]
n = int(raw_input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]
x_bat, y_bat = x0, y0

solver = SolverWithAACut((w, h), (x0, y0))
print >> sys.stderr, "solver:\n", solver

# game loop
while 1:
    bomb_dist = raw_input()  # Current distance to the bomb compared to previous distance (COLDER, WARMER, SAME or UNKNOWN)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    x_bat, y_bat = solver.compute_next_position(bomb_dist)
    print >> sys.stderr, "\nsolver:\n", solver

    print "%d %d" % (x_bat, y_bat)
