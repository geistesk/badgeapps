import color
import display
import utime
import urandom


COLORS = [(0, 153, 51), (0, 153, 0), (51, 204, 51), (0, 102, 0), (102, 255, 102)]
LINES = 40


class Line:
    def __init__(self):
        self._x = urandom.randint(0, 160)
        self._y = urandom.randint(0, 20)
        self._speed = urandom.randint(1, 15)
        self._elems = []

    def update_check(self):
        self._y += self._speed
        self._elems.append(urandom.choice(COLORS))

        return self._y < 80

    def __iter__(self):
        self._iter_id = 0
        return self

    def __next__(self):
        if self._iter_id >= len(self._elems):
            raise StopIteration
        elif self._y + self._iter_id >= 80:
            raise StopIteration
        else:
            col = self._elems[self._iter_id]
            self._iter_id += 1
            return ((self._x, self._y + self._iter_id), col)


class LineManager:
    def __init__(self):
        self._lines = []
        for l in range(LINES):
            self._lines.append(Line())

    def draw(self):
        with display.open() as disp:
            disp.clear()

            for i in range(LINES):
                if not self._lines[i].update_check():
                    self._lines[i] = Line()

                for p in self._lines[i]:
                    disp.pixel(p[0][0], p[0][1],
                            col=color.Color(p[1][0], p[1][1], p[1][2]))

            disp.update()


lm = LineManager()
while True:
    lm.draw()
    utime.sleep(0.05)
