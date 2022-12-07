import command as cmd
import consts

# TODO: swap x, y order

class Tile:
    def __init__(self, y, x, color) -> None:
        self.y = y
        self.x = x
        self.color = color

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        pass


class Pink(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "pink")


class Red(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "red")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.unmove()
        ip.turn()
        ip.move(level)


class Yellow(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "yellow")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.unmove()
        ip.turn()
        ip.turn()


class Purple(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "purple")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.move(level)
        ip.flavor = "lemon"


class Green(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "green")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        print('activate')
        for vec in consts.DIRS:
            pos = (self.y + vec[0], self.x + vec[1])
            if level.grid[pos].color == "pink":
                level.grid[pos] = Yellow(pos[0], pos[1])
            if level.grid[pos].color == "yellow":
                level.grid[pos] = Pink(pos[0], pos[1])


class Orange(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "orange")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        ip.flavor = "orange"


class Blue(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "blue")
        self.electrified = False

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        if ip.flavor == "orange" or self.electrified:
            ip.unmove()
            ip.turn()
            ip.turn()
            ip.move(level)


class Start(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "start")


class End(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "end")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        level.stop()


class Empty(Tile):
    def __init__(self, y, x) -> None:
        super().__init__(y, x, "black")

    def activate(self, ip: cmd.InstructionPointer, level: cmd.Level):
        level.ips.remove(ip)
