from math   import sin, cos, radians
from random import randint, seed, uniform
from time   import sleep
import ugfx

EDGE_RIGHT_DOWN = (296, 128)

def tree(point, level, angle):
    if level > 0:
        point_new = (
          point[0] + int(cos(radians(angle)) * level * 3.2),
          point[1] + int(sin(radians(angle)) * level * 2.0))
        rand_left, rand_right = (uniform(0.5, 1.5), uniform(0.5, 1.5))

        ugfx.line(point[0], point[1], point_new[0], point_new[1], ugfx.WHITE)
        tree(point_new, level - 1, angle - 20 * rand_left)
        tree(point_new, level - 1, angle + 20 * rand_right)

ugfx.init()
ugfx.clear(ugfx.WHITE)
ugfx.flush()
ugfx.clear(ugfx.BLACK)
ugfx.flush()

ugfx.input_init()
ugfx.input_attach(ugfx.BTN_A, lambda p: quit(p))
ugfx.input_attach(ugfx.BTN_B, lambda p: quit(p))
ugfx.input_attach(ugfx.BTN_START, lambda p: quit(p))
ugfx.input_attach(ugfx.BTN_SELECT, lambda p: quit(p))

while True:
    for i in range(0, randint(4, 8)):
        tree(EDGE_RIGHT_DOWN, randint(4, 14), -155)
        sleep(randint(3, 13) * 0.1)
        ugfx.flush()
    ugfx.clear(ugfx.BLACK)
    ugfx.flush()
