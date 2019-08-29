SHA17, CCC19, BADGE = 0, 1, None
try:
    import ugfx
    BADGE = SHA17
except:
    import display
    BADGE = CCC19


if BADGE == SHA17:
    import ugfx
    from math   import sin, cos, radians
    from random import randint, seed, uniform
    from time   import sleep

    EDGE_RIGHT_DOWN = (296, 128)
elif BADGE == CCC19:
    import display
    from math    import sin, cos, radians
    from urandom import randint, seed, uniform
    from utime   import sleep

    EDGE_RIGHT_DOWN = (159, 79)


def sanitize_point(point):
    f = lambda x, no: max(min(EDGE_RIGHT_DOWN[no], x), 0)
    return (f(point[0], 0), f(point[1], 1))


def tree(point, level, angle, disp):
    if level > 0:
        point_new = (
            point[0] + int(cos(radians(angle)) * level * 3.2),
            point[1] + int(sin(radians(angle)) * level * 2.0))
        rand_left, rand_right = (uniform(0.5, 1.5), uniform(0.5, 1.5))

        if BADGE == SHA17:
            ugfx.line(point[0], point[1], point_new[0], point_new[1], ugfx.WHITE)
        elif BADGE == CCC19:
            p0, p1 = sanitize_point(point), sanitize_point(point_new)
            disp.line(p0[0], p0[1], p1[0], p1[1], col=(128, 128, 128))

        tree(point_new, level - 1, angle - 20 * rand_left, disp)
        tree(point_new, level - 1, angle + 20 * rand_right, disp)


if BADGE == SHA17:
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

    disp = None
elif BADGE == CCC19:
    disp = display.open()

while True:
    for i in range(0, randint(4, 8)):
        tree(EDGE_RIGHT_DOWN, randint(4, 14), -155, disp)

        if BADGE == SHA17:
            sleep(randint(3, 13) * 0.1)
            ugfx.flush()
        elif BADGE == CCC19:
            disp.update()
            sleep(0.1)

    if BADGE == SHA17:
        ugfx.clear(ugfx.BLACK)
        ugfx.flush()
    elif BADGE == CCC19:
        sleep(0.5)
        disp.clear().update()
