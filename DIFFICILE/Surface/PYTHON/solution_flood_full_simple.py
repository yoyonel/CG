from collections import defaultdict


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
            return (self.get_tile_type(x, y) != '#') & (not self.tile_has_id(x, y))
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
        while (list_coords):
            coord = list_coords.pop()
            list_neighboors = self.update_id_for_one_tile(coord[0], coord[1])
            list_coords.extend(list_neighboors)

    def get_area(self, x, y):
        #
        return self.area_for_id[self.get_tile_id(x, y)]


class MapForCG(MapForFloodFilling):
    """ """
    def solve(self, x, y):
        #
        if self.get_tile_type(x, y) == '#':
            # ce n'est pas un lac donc 0 de suface
            return 0
        elif self.tile_has_id(x, y):
            # deja calcule
            return self.area_for_id[self.get_tile_id(x, y)]
        else:
            # pas encore calcule
            # on propoge l'id du lac (mise a jour de la map d'id et maj de l'aire)
            self.update_id_with_propagation(x, y)
            # on passe a l'id suivant (pour les prochaines identification de lacs)
            self.cur_id += 1
            # on renvoie l'aire du lac identifie
            return self.get_area(x, y)

# map dimensions
l = int(raw_input())
h = int(raw_input())

# map
map_tiles = MapForCG(l, h)
for i in xrange(h):
    row = raw_input()
    #
    map_tiles.append_row(row)

# requests coordinates
n = int(raw_input())
for i in xrange(n):
    x, y = [int(j) for j in raw_input().split()]
    #
    print map_tiles.solve(x, y)

