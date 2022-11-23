class Tape:
    def __init__(self) -> None:
        self.pointer = 0
        self._tape = [0]

    def move(self, step):
        self.pointer += step
        while self.pointer >=len(self._tape):
            self._tape.append(0)
        while self.pointer < 0:
            self._tape.insert(0, 0)
            self.pointer += 1

    def add(self, num):
        self._tape[self.pointer] += num

    def peek(self):
        return self._tape[self.pointer]


if __name__ == "__main__":
    tape = Tape()
    tape.add(2)
    tape.move(-2)
    print(tape._tape,tape.pointer)
    tape.move(5)
    print(tape._tape,tape.pointer)
