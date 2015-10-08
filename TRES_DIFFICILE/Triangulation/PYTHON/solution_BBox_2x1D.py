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
        return "Range(%d,%d)" % (self.start, self.end)


class SolverWithAACut:
    #
    def __init__(self, _w, _h, _x, _y, _bomb_dist = 'UNKNOWN'):
        """

        :param w:
        :param h:
        :return:
        """
        #
        #self.xRange = Range(0.5, (_w-1)-0.5)
        #self.yRange = Range(0.5, (_h-1)-0.5)
        self.xRange = Range(0, _w - 1)
        self.yRange = Range(0, _h - 1)
        self.initial_dimensions = (self.xRange, self.yRange)
        #
        self.position = (_x, _y)
        self.last_position = None
        #
        self.bomb_dist = _bomb_dist
        #
        self.cut_position = None
        self.type_cut = None

    def update_ranges(self, _bomb_dist):
        """

        :param _bomb_dist:
        :return:
        """

        if _bomb_dist == 'SAME':
            # cut_position forcement sur une cellule
            if self.type_cut == 'VERTICAL':
                # une seule colonne nous interesse
                self.xRange = Range(self.cut_position, self.cut_position)
            else:
                # une seule ligne nous interesse
                self.yRange = Range(self.cut_position, self.cut_position)
            # on passe en recherche unidimensionnelle 1D
        elif _bomb_dist == 'WARMER':
            if self.type_cut == 'VERTICAL':
                if self.position[0] > self.cut_position:
                    self.xRange.start = self.cut_position + self.position_on_cell(self.cut_position)
                else:
                    self.xRange.end = self.cut_position - self.position_on_cell(self.cut_position)
            else:
                if self.position[1] > self.cut_position:
                    self.yRange.start = self.cut_position + self.position_on_cell(self.cut_position)
                else:
                    self.yRange.end = self.cut_position - self.position_on_cell(self.cut_position)
        elif _bomb_dist == 'COLDER':
            if self.type_cut == 'VERTICAL':
                if self.last_position[0] > self.cut_position:
                    self.xRange.start = self.cut_position + self.position_on_cell(self.cut_position)
                else:
                    self.xRange.end = self.cut_position - self.position_on_cell(self.cut_position)
            else:
                if self.last_position[1] > self.cut_position:
                    self.yRange.start = self.cut_position + self.position_on_cell(self.cut_position)
                else:
                    self.yRange.end = self.cut_position - self.position_on_cell(self.cut_position)
        # else _bomb_dist == 'UNKNOWN' => rien a faire

    @staticmethod
    def position_on_cell(_position):
        """

        :param _position:
        :return:
        """
        return _position != int(_position)

    @staticmethod
    def compute_central_symmetry(position, center):
        """

        :param position:
        :param center:
        :return:
        """
        return 2.0*center - position

    def compute_cut(self, _range, _position, _init_range):
        """
        :param _range:
        :return:
        """
        center = _range.center()

        # calcul de la symetrie de central de la position
        # et clamp de la valeur par le range (dimension) initial(e)
        central_symmetry = _init_range.clamp(self.compute_central_symmetry(_position, center))
        
        # on maj le centre par rapport a cette symetrie
        #center = (_position + central_symmetry) * 0.5
        center = (_position + central_symmetry) // 2

        #center_on_cell = False
        # est ce que le centre courant choisit est sur une interligne ou une case ?
        '''
        if not self.position_on_cell(center):
            # si le centre est sur une interligne
            # on voit si on peut le deplacer pour se trouver sur une cellule
            distance_cs_to_end = _range.end - central_symmetry
            if distance_cs_to_end >= 1:
                # update center et la symetrie centrale
                center += 0.5
                central_symmetry += 1
                #center_on_cell = True
        '''
        # on renvoie les resultats
        #return central_symmetry, center, center_on_cell
        return central_symmetry, center

    def compute_vertical_cut(self):
        """

        :return:
        """
        return self.compute_cut(self.xRange, self.position[0], self.initial_dimensions[0])

    def compute_horizontal_cut(self):
        """

        :return:
        """
        return self.compute_cut(self.yRange, self.position[1], self.initial_dimensions[1])

    def compute_next_position(self, _bomb_dist):
        """

        :return:
        """
        # maj des ranges par rapport a la reponse du scanner de Batman
        self.update_ranges(_bomb_dist)

        print >> sys.stderr, "-> ", self.xRange.isUnit(), self.yRange.isUnit()
		# est ce que les ranges sont reduites a l'unite ?
        if self.xRange.isUnit() & self.yRange.isUnit():
            print >> sys.stderr, "UNITES pour les ranges!"
			# si oui, on a la solution du probleme
            next_position = (self.xRange.start, self.yRange.start)
        else:
            # on calcul la prochaine position pour effectuer un cut (horizontal ou vertical)
            if self.xRange.len() > self.yRange.len():
                results_cut = self.compute_vertical_cut()
                type_cut = 'VERTICAL'
                next_position = (results_cut[0], self.position[1])
            else:
                results_cut = self.compute_horizontal_cut()
                type_cut = 'HORIZONTAL'
                next_position = (self.position[0], results_cut[0])
                
            cut_position = results_cut[1]
            
            self.last_position = self.position
            self.position = next_position
            self.cut_position = cut_position
            self.type_cut = type_cut

        return next_position

    # String representaion (for debugging)
    def __repr__(self):
        return 'ranges: %s - %s\nlast_position: %s\nposition: %s\ncut_position: %s\ntype_cut: %s' % (
            self.xRange, self.yRange,
            self.last_position,
            self.position,
            self.cut_position,
            self.type_cut
        )

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.


w, h = [int(i) for i in raw_input().split()]
n = int(raw_input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]
x_bat, y_bat = x0, y0

solver = SolverWithAACut(w, h, x0, y0)
print >> sys.stderr, "solver:\n", solver

# game loop
while 1:
    bomb_dist = raw_input()  # Current distance to the bomb compared to previous distance (COLDER, WARMER, SAME or UNKNOWN)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    x_bat, y_bat = solver.compute_next_position(bomb_dist)
    print >> sys.stderr, "\nsolver:\n", solver

    print "%d %d" % (x_bat, y_bat)
