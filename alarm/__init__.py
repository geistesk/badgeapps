import display
import interrupt
import utime
import vibra

class Alarm:
    def __init__(self, limit):
        self._limit = limit

        interrupt.set_callback(interrupt.RTC_ALARM, self._alarm_handler)
        interrupt.enable_callback(interrupt.RTC_ALARM)

        self._display_time()
        utime.alarm(utime.time() + 1)

    def _alarm_handler(self, x):
        self._limit -= 1
        if self._limit == 0:
            self._display("uwu")
            vibra.vibrate(200)
        else:
            self._display_time()
            utime.alarm(utime.time() + 1)

    def _display(self, msg):
        with display.open() as disp:
            disp.clear()
            disp.print("{}".format(msg))
            disp.update()
            disp.close()

    def _display_time(self):
        self._display("T-{}".format(self._limit))


Alarm(5)

while True:
    pass
