import numpy as np
import command as cmd
import consts


class Tile:
    def __init__(self, x, y, color) -> None:
        self.x = x
        self.y = y
        self.color = color

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        pass

    def update(self):
        pass


class Pink(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "pink")


class Red(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "red")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.unmove()
        ip.turn()


class Yellow(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "yellow")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.unmove()
        ip.turn()
        ip.turn()


class Purple(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "purple")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.move()
        ip.flavor = "lemon"


class Green(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "green")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        for vec in consts.DIRS:
            pos = (self.y + vec[0], self.x + vec[1])
            if level.map[pos].color == "pink":
                level.map[pos] = Yellow(pos[1], pos[0])
            if level.map[pos].color == "yellow":
                level.map[pos] = Pink(pos[1], pos[0])


class Orange(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "orange")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.flavor = "orange"


class Blue(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "blue")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        touching_yellow = any(
            [level.map[self.y + vec[1], self.x + vec[0]] for vec in consts.DIRS]
        )
        if ip.flavor == "orange" or touching_yellow:
            ip.unmove()
            ip.turn()
            ip.turn()


class Start(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "start")


class End(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "end")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        level.end()


class Empty(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "empty")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        level.ips.remove(ip)
