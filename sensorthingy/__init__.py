import buttons
import display
import os
import utime

from apps.sensorthingy import manager, sensors


TIMEOUT_SEC = 15


def welcome_msg():
    with display.open() as disp:
        disp.clear()
        disp.print("Press")
        disp.print("any key", posy=22)
        disp.print("to exit", posy=44)
        disp.update()


def backlight_brightness(x):
    with display.open() as disp:
        disp.clear()
        disp.backlight(x)
        disp.update()


def main():
    welcome_msg()
    utime.sleep(2)

    backlight_brightness(0)

    sensor_manager = manager.SensorManager(sensors.sensors)
    c = 0

    while True:
        if c == TIMEOUT_SEC:
            c = 0
            sensor_manager.dump_log()

        pressed = buttons.read(buttons.TOP_LEFT | buttons.TOP_RIGHT |
                buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)
        if pressed != 0:
            break

        utime.sleep(1)
        c += 1

    backlight_brightness(50)


main()
os.exit(0)
