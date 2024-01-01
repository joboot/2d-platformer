import pygame

#
NEIGHBOR_OFFSETS = [
                    (-1, 1), (-1, 0), (-1, -1),
                    (1, 1), (1, 0), (1, -1),
                    (0, 1), (0, 0), (0, -1)
                    ]
# List of tiles used
PHYSICS_TILES = {'grass', 'stone'}


# Creation of tilemap object
class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        # Creation of blocks onto tilemap
        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    # Detects tiles around entity
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size)), (int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    # Detects rects around that have physics/collision
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(float(tile['pos'][0] * self.tile_size),
                                         float(tile['pos'][1] * self.tile_size),
                                         self.tile_size,
                                         self.tile_size))
        return rects

    # Renders tiles in tilemap
    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']],
                              (int(tile['pos'][0] * self.tile_size) - offset[0],
                              int(tile['pos'][1] * self.tile_size) - offset[1]))

        #
        # for loc in self.tilemap:
        #     tile = self.tilemap[loc]
        #     surf.blit(self.game.assets[tile['type']][tile['variant']],
        #               (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
