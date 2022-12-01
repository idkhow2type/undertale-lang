import consts
import numpy as np
from PIL import Image
from pprint import pprint


class InstructionPointer:
    def __init__(self, x: int, y: int, direction: int, flavor: str) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.vec = consts.DIRS[self.direction]
        self.flavor = flavor

    def move(self, grid):
        self.x += self.vec[0]
        self.y += self.vec[1]

        grid[self.y, self.x].activate(self, grid)

    def turn(self):
        self.direction = (self.direction + 1) % len(consts.DIRS)
        self.vec = consts.DIRS[self.direction]

    def unmove(self):
        self.x -= self.vec[0]
        self.y -= self.vec[1]


class Level:
    def __init__(self, image: Image) -> None:
        import tiles

        img_arr = np.array(image)
        self.image = image
        self.grid = np.empty(
            shape=(img_arr.shape[0], img_arr.shape[1]), dtype=tiles.Tile
        )
        self.ips = []
        self.ticks = 0

        for iy, ix, _ in np.ndindex(img_arr.shape):
            if np.all(img_arr[iy, ix] == consts.COLORS["pink"]):
                self.grid[iy, ix] = tiles.Pink(ix, iy)
            elif np.all(img_arr[iy, ix] == consts.COLORS["red"]):
                self.grid[iy, ix] = tiles.Red(ix, iy)
            elif np.all(img_arr[iy, ix] == consts.COLORS["yellow"]):
                self.grid[iy, ix] = tiles.Yellow(ix, iy)
            elif np.all(img_arr[iy, ix] == consts.COLORS["purple"]):
                self.grid[iy, ix] = tiles.Purple(ix, iy)
            elif np.all(img_arr[iy, ix] == consts.COLORS["green"]):
                self.grid[iy, ix] = tiles.Green(ix, iy)
            elif np.all(img_arr[iy, ix] == consts.COLORS["orange"]):
                self.grid[iy, ix] = tiles.Orange(ix, iy)
            elif np.all(img_arr[iy, ix] == consts.COLORS["blue"]):
                self.grid[iy, ix] = tiles.Blue(ix, iy)
            else:
                self.grid[iy, ix] = tiles.Empty(ix, iy)

    def tick(self):
        if self.ticks % 2 == 0:
            self.ips.append(InstructionPointer(1, 1, 0, None))

        for ip in self.ips:
            ip.move(self.grid)

    def show(self):
        self.grid

    def end(self):
        quit()
