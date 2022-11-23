import consts
import numpy as np
import tiles


class InstructionPointer:
    def __init__(self, x, y, direction, flavor) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.move_vctr = consts.DIRS[self.direction]
        self.flavor = flavor

    def move(self, level: np.ndarray[tiles.Tile]):
        self.x += self.move_vctr[0]
        self.y += self.move_vctr[1]

        level[self.y, self.x].activate()

    def turn(self):
        self.direction = (self.direction + 1) % len(consts.DIRS)
        self.move_vctr = consts.DIRS[self.direction]

    def unmove(self):
        self.x -= self.move_vctr[0]
        self.y -= self.move_vctr[1]
