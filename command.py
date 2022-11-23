import consts
import numpy as np
import tiles


class Level:
    def __init__(self, image) -> None:
        self.image = image
        self.map = np.asarray(image)
        self.ips = []
        self.ticks = 0
        self.start = tiles.Start(1, 1)
        self.end = self.map[(s - 2 for s in self.map.shape)]

        self.map[1, 1] = self.start
        self.map[self.end.y, self.end.x] = self.end
        for iy, ix in np.ndindex(self.map.shape):
            if self.map[iy, ix] == "pink":
                self.map[iy, ix] = tiles.Pink(ix, iy)
            if self.map[iy, ix] == "red":
                self.map[iy, ix] = tiles.Red(ix, iy)
            if self.map[iy, ix] == "yellow":
                self.map[iy, ix] = tiles.Yellow(ix, iy)
            if self.map[iy, ix] == "purple":
                self.map[iy, ix] = tiles.Purple(ix, iy)
            if self.map[iy, ix] == "green":
                self.map[iy, ix] = tiles.Green(ix, iy)
            if self.map[iy, ix] == "orange":
                self.map[iy, ix] = tiles.Orange(ix, iy)
            if self.map[iy, ix] == "blue":
                self.map[iy, ix] = tiles.Blue(ix, iy)

    def tick(self):
        if self.ticks % 2 == 0:
            self.ips.append(InstructionPointer(1, 1, 0, None))

        for ip in self.ips:
            ip.move(self.map)

    def end(self):
        quit()


class InstructionPointer:
    def __init__(self, x, y, direction, flavor) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.vec = consts.DIRS[self.direction]
        self.flavor = flavor

    def move(self, level: Level):
        self.x += self.vec[0]
        self.y += self.vec[1]

        level[self.y, self.x].activate(self, level)

    def turn(self):
        self.direction = (self.direction + 1) % len(consts.DIRS)
        self.vec = consts.DIRS[self.direction]

    def unmove(self):
        self.x -= self.vec[0]
        self.y -= self.vec[1]
