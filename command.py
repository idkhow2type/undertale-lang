import consts
import numpy as np
from PIL import Image, ImageDraw
from pprint import pprint


class InstructionPointer:
    def __init__(self, x: int, y: int, direction: int, flavor: str) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.vec = consts.DIRS[self.direction]
        self.flavor = flavor

    def move(self, level):
        self.x += self.vec[0]
        self.y += self.vec[1]

        level.grid[self.y, self.x].activate(self, level)

    def turn(self):
        self.direction = (self.direction + 1) % len(consts.DIRS)
        self.vec = consts.DIRS[self.direction]

    def unmove(self):
        self.x -= self.vec[0]
        self.y -= self.vec[1]


class Level:
    def __init__(self, image: Image) -> None:
        import tiles

        self.image = image
        self.parse_image(image)
        self.start = (1, 1)
        self.end = (1, self.grid.shape[1] - 2)
        self.grid[self.start] = tiles.Start(self.start[1], self.start[0])
        self.grid[self.end] = tiles.End(self.end[1], self.end[0])
        self.ips = []
        self.ticks = 0
        self.yellows = {}
        self.get_yellows()

    def parse_image(self, image: Image):
        import tiles

        self.img_arr = np.array(image)
        self.grid = np.empty(
            shape=(self.img_arr.shape[0], self.img_arr.shape[1]), dtype=tiles.Tile
        )

        for iy, ix, _ in np.ndindex(self.img_arr.shape):
            if np.all(self.img_arr[iy, ix] == consts.COLORS["pink"]):
                self.grid[iy, ix] = tiles.Pink(ix, iy)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["red"]):
                self.grid[iy, ix] = tiles.Red(ix, iy)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["yellow"]):
                self.grid[iy, ix] = tiles.Yellow(ix, iy)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["purple"]):
                self.grid[iy, ix] = tiles.Purple(ix, iy)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["green"]):
                self.grid[iy, ix] = tiles.Green(ix, iy)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["orange"]):
                self.grid[iy, ix] = tiles.Orange(ix, iy)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["blue"]):
                self.grid[iy, ix] = tiles.Blue(ix, iy)
            else:
                self.grid[iy, ix] = tiles.Empty(ix, iy)

    def get_yellows(self):
        for iy, ix in np.ndindex(self.grid.shape):
            if self.grid[iy, ix].color == "yellow":
                self.yellows[(iy, ix)] = self.get_same_colors((iy, ix), "blue")
            elif self.grid[iy, ix].color == "green":
                for vec in consts.DIRS:
                    y = iy + vec[0]
                    x = ix + vec[1]
                    if self.grid[y, x].color == "pink":
                        self.yellows[(y, x)] = self.get_same_colors((iy, ix), "blue")

    def get_same_colors(self, root_tile: tuple, color: str, tiles: list = []):
        neighbors = []

        for vec in consts.DIRS:
            y = root_tile[0] + vec[0]
            x = root_tile[1] + vec[1]

            if (y, x) not in tiles and self.grid[y, x].color == color:
                neighbors.append((y, x))

        tiles.extend(neighbors)
        for tile in neighbors:
            neighbors.extend(self.get_same_colors(tile, color, tiles))

        return neighbors

    def tick(self):
        for ip in self.ips:
            ip.move(self)

        if self.ticks % 2 == 0:
            self.ips.append(InstructionPointer(self.start[1], self.start[0], 0, None))

        self.ticks += 1

    def stop(self):
        print("quitting...")
        self.show()
        quit()

    def show(self, scale=5):
        image = self.image.resize(
            (self.image.size[0] * scale, self.image.size[1] * scale),
            resample=Image.Resampling.BOX,
        )
        draw = ImageDraw.Draw(image)
        for ip in self.ips:
            bound = (
                ip.x * scale + 1,
                ip.y * scale + 1,
                (ip.x + 1) * scale - 2,
                (ip.y + 1) * scale - 2,
            )
            draw.ellipse(
                bound, fill=(196, 79, 0) if ip.flavor == "orange" else (106, 47, 106)
            )
        image.show()