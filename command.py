import consts
import numpy as np
import tiles
from PIL import Image


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
        self.image = image
        self.grid = np.asarray(image)
        self.ips = []
        self.ticks = 0
        self.start = tiles.Start(1, 1)
        self.end = self.grid[(s - 2 for s in self.grid.shape)]

        self.grid[1, 1] = self.start
        self.grid[self.end.y, self.end.x] = self.end
        for iy, ix in np.ndindex(self.grid.shape):
            if self.grid[iy, ix] == consts.COLORS["pink"]:
                self.grid[iy, ix] = tiles.Pink(ix, iy)
            elif self.grid[iy, ix] == consts.COLORS["red"]:
                self.grid[iy, ix] = tiles.Red(ix, iy)
            elif self.grid[iy, ix] == consts.COLORS["yellow"]:
                self.grid[iy, ix] = tiles.Yellow(ix, iy)
            elif self.grid[iy, ix] == consts.COLORS["purple"]:
                self.grid[iy, ix] = tiles.Purple(ix, iy)
            elif self.grid[iy, ix] == consts.COLORS["green"]:
                self.grid[iy, ix] = tiles.Green(ix, iy)
            elif self.grid[iy, ix] == consts.COLORS["orange"]:
                self.grid[iy, ix] = tiles.Orange(ix, iy)
            elif self.grid[iy, ix] == consts.COLORS["blue"]:
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
