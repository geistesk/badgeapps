import buttons
import color
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

    def _display_time(self):
        self._display("T-{}".format(self._limit))


class SetupMenu:
    def __init__(self):
        self._time_val = 0

    def get_alarm(self):
        while True:
            self._show_setup_time()

            pressed = buttons.read(
                    buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT)
            if pressed & buttons.BOTTOM_LEFT != 0:
                self._time_val = max(0, self._time_val - 15)
            elif pressed & buttons.BOTTOM_RIGHT != 0:
                self._time_val += 15
            elif pressed & buttons.TOP_RIGHT != 0:
                return Alarm(self._time_val)

    def _show_setup_time(self):
        col_text_bg = color.Color(0, 0, 255)
        col_text_fg = color.Color(255, 255, 255)
        col_time_bg = color.Color(0, 128, 255)
        col_time_fg = color.Color(255, 255, 255)

        t_min, t_sec = int(self._time_val / 60), int(self._time_val % 60)
        t_msg = "{:02d} : {:02d}".format(t_min, t_sec)

        with display.open() as disp:
            disp.clear(col_text_bg)
            disp.print("set alarm", fg=col_text_fg, bg=col_text_bg, posx=17)
            disp.rect(0, 20, 160, 60, col=col_time_bg)
            disp.print(t_msg, fg=col_time_fg, bg=col_time_bg, posx=35, posy=30)
            disp.update()


alarm = SetupMenu().get_alarm()
while True:
    pass
