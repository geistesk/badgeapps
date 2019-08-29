import color
import display
import leds
import urandom
import utime
import os


COLORS = [(0, 153, 51), (0, 153, 0), (51, 204, 51), (0, 102, 0), (102, 255, 102)]
LINE_AMOUNT = 50
DELAY_SEC = 0.03


class Drawer:
    "Drawer is a interface-like class with the draw method for the display."
    def draw(self, disp):
        pass


class Line:
    "A simple matrix-like Line, is used by the LineDrawer."
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


class LineDrawer(Drawer):
    "LineDrawer draws multiple Lines for the matrix-like background."
    def __init__(self):
        self._lines = []
        for l in range(LINE_AMOUNT):
            self._lines.append(Line())

    def draw(self, disp):
        for i in range(LINE_AMOUNT):
            if not self._lines[i].update_check():
                self._lines[i] = Line()

            for p in self._lines[i]:
                disp.pixel(p[0][0], p[0][1],
                        col=color.Color(p[1][0], p[1][1], p[1][2]))


class NickDrawer(Drawer):
    FILENAME = 'nickname.txt'

    def __init__(self):
        if NickDrawer.FILENAME in os.listdir("."):
            f = open(NickDrawer.FILENAME, 'r')
            self._nick = f.read()
            f.close()
        else:
            self._nick = "No {}".format(NickDrawer.FILENAME)

    def draw(self, disp):
        disp.print(self._nick, fg=urandom.choice(COLORS),
                posx=80 - round(len(self._nick) / 2 * 14), posy=30)


def matrix_leds():
    for l in range(15):
        leds.set(l, urandom.choice(COLORS))


ld = LineDrawer()
nd = NickDrawer()

while True:
    matrix_leds()

    with display.open() as disp:
        disp.clear()
        ld.draw(disp)
        nd.draw(disp)
        disp.update()

    utime.sleep(DELAY_SEC)
