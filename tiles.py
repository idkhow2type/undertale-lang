import numpy as np
import code
import memory
import consts


class Tile:
    def __init__(self, x, y, color) -> None:
        self.x = x
        self.y = y
        self.color = color

    def activate(self, ip):
        pass


class Pink(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "pink")

    def activate(self, ip: code.InstructionPointer):
        pass


class Red(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "red")

    def activate(self, ip: code.InstructionPointer):
        ip.unmove()
        ip.turn()


class Yellow(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "yellow")

    def activate(self, ip: code.InstructionPointer):
        ip.unmove()
        ip.turn()
        ip.turn()


class Purple(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "purple")

    def activate(self, ip: code.InstructionPointer):
        ip.move()
        ip.flavor = "lemon"


class Green(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "green")

    def activate(self, ip: code.InstructionPointer, tape: memory.Tape):
        if ip.direction == 0:
            tape.move(1)
        if ip.direction == 2:
            tape.move(-1)
        if ip.direction == 1:
            tape.add(-1)
        if ip.direction == 3:
            tape.move(1)


class Orange(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "orange")

    def activate(self, ip: code.InstructionPointer, tape: memory.Tape):
        if tape.peek() == 0:
            ip.flavor = "orange"


class Blue(Tile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, "blue")

    def activate(self, ip: code.InstructionPointer, level: np.ndarray[Tile]):
        touching_yellow = any([level[self.y + direc[1], self.x + direc[0]] for direc in consts.DIRS])
        if ip.flavor == 'orange' or touching_yellow:
            ip.unmove()
            ip.turn()
            ip.turn()
