import consts
import numpy as np
from PIL import Image, ImageDraw
from pprint import pprint


class InstructionPointer:
    def __init__(self, y: int, x: int, direction: int, flavor: str) -> None:
        self.y = y
        self.x = x
        self.direction = direction
        self.vec = consts.DIRS[self.direction]
        self.flavor = flavor

    def move(self, level):
        self.y += self.vec[0]
        self.x += self.vec[1]

        level.grid[self.y, self.x].activate(self, level)

    def turn(self):
        self.direction = (self.direction + 1) % len(consts.DIRS)
        self.vec = consts.DIRS[self.direction]

    def unmove(self):
        self.y -= self.vec[0]
        self.x -= self.vec[1]


class Level:
    def __init__(self, image: Image) -> None:
        import tiles

        self.parse_image(image)
        self.start = (1, 1)
        self.end = (1, self.grid.shape[1] - 2)
        self.grid[self.start] = tiles.Start(self.start[0], self.start[1])
        self.grid[self.end] = tiles.End(self.end[0], self.end[1])
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
                self.grid[iy, ix] = tiles.Pink(iy, ix)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["red"]):
                self.grid[iy, ix] = tiles.Red(iy, ix)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["yellow"]):
                self.grid[iy, ix] = tiles.Yellow(iy, ix)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["purple"]):
                self.grid[iy, ix] = tiles.Purple(iy, ix)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["green"]):
                self.grid[iy, ix] = tiles.Green(iy, ix)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["orange"]):
                self.grid[iy, ix] = tiles.Orange(iy, ix)
            elif np.all(self.img_arr[iy, ix] == consts.COLORS["blue"]):
                self.grid[iy, ix] = tiles.Blue(iy, ix)
            else:
                self.grid[iy, ix] = tiles.Empty(iy, ix)

    def get_yellows(self):
        for iy, ix in np.ndindex(self.grid.shape):
            if self.grid[iy, ix].color == "yellow":
                self.yellows[(iy, ix)] = self.get_same_colors((iy, ix), "blue")
            elif self.grid[iy, ix].color == "green":
                for vec in consts.DIRS:
                    y = iy + vec[0]
                    x = ix + vec[1]
                    if self.grid[y, x].color == "pink":
                        self.yellows[(y, x)] = self.get_same_colors((y, x), "blue")

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
        for k, v in self.yellows.items():
            for tile in v:
                self.grid[tile].electrified = self.grid[k].color == "yellow"

        for ip in self.ips:
            ip.move(self)

        if self.ticks % 2 == 0:
            self.ips.append(InstructionPointer(self.start[0], self.start[1], 0, None))

        self.ticks += 1

    def stop(self):
        print("quitting...")
        self.create_image().show()
        quit()

    def create_image(self, scale=5):
        min_scale = 4

        if scale < min_scale:
            raise ValueError(f"Scale must be greater or equal to {min_scale}")

        image = Image.new(mode="RGB", size=self.grid.shape[::-1])
        pixels = image.load()
        for y, x in np.ndindex(self.grid.shape):
            # TODO: change color consts to tuple
            pixels[x, y] = tuple(consts.COLORS[self.grid[y, x].color])

        image = image.resize(
            (image.size[0] * scale, image.size[1] * scale),
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

        return image
