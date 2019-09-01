import display
import utime

from apps.sensorthingy import manager, sensors


TIMEOUT_SEC = 15


def disable_display():
    with display.open() as disp:
        disp.clear()
        disp.backlight(0)
        disp.update()


def main():
    disable_display()

    sens = [sensors.EnvironmentalSensor(),
            sensors.LightSensor(),
            sensors.PowerSensor()]
    sm = manager.SensorManager(sens)

    while True:
        sm.dump_log()
        utime.sleep(TIMEOUT_SEC)


main()
