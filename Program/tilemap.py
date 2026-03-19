import pygame

class TileMap():
    def __init__(self, level):
        self.tiles = []
        self.tile_size = 40

        # return index and value at index
        # then iterate through level
        for row_i, row in enumerate(level):
            # for each row check each column
            for col_i, tile in enumerate(row):
                # if tile present in tile map
                if tile == "1":
                    # create a tile
                    rect = pygame.Rect(
                        col_i * self.tile_size,
                        row_i * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    # store the tiles in a list
                    self.tiles.append(rect)
                    # this is so we can draw them easily
    def draw(self, screen):
        # draw all tiles in the list of tiles
        for tile in self.tiles:
            pygame.draw.rect(screen, (100,200,100), tile)