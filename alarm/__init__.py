import buttons
import color
import display
import interrupt
import utime
import vibra

def show_time(t):
    col_text_bg = color.Color(0, 0, 255)
    col_text_fg = color.Color(255, 255, 255)
    col_time_bg = color.Color(0, 128, 255)
    col_time_fg = color.Color(255, 255, 255)

    t_min, t_sec = int(t / 60), int(t % 60)
    t_msg = "{:02d} : {:02d}".format(t_min, t_sec)

    with display.open() as disp:
        disp.clear(col_text_bg)
        disp.print("alarm", fg=col_text_fg, bg=col_text_bg, posx=47)
        disp.rect(0, 20, 160, 60, col=col_time_bg)
        disp.print(t_msg, fg=col_time_fg, bg=col_time_bg, posx=35, posy=30)
        disp.update()


class Alarm:
    def __init__(self, limit):
        self._limit = limit
        self._done = False

        interrupt.set_callback(interrupt.RTC_ALARM, self._countdown_handler)
        interrupt.enable_callback(interrupt.RTC_ALARM)

        utime.alarm(utime.time() + 1)

    def _countdown_handler(self, x):
        self._limit = max(0, self._limit - 1)
        show_time(self._limit)

        if self._limit > 0:
            utime.alarm(utime.time() + 1)
        else:
            self._alarm_handler()

    def _alarm_handler(self):
        interrupt.disable_callback(interrupt.RTC_ALARM)

        vibra.set(True)
        while True:
            pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | \
                    buttons.TOP_RIGHT | buttons.TOP_LEFT)
            if pressed != 0:
                break

        vibra.set(False)
        self._done = True

    def wait(self):
        while not self._done:
            pass


class SetupMenu:
    def __init__(self):
        self._time_val = 0

    def start_alarm(self):
        while True:
            show_time(self._time_val)

            pressed = buttons.read(
                    buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT)
            if pressed & buttons.BOTTOM_LEFT != 0:
                self._time_val = max(0, self._time_val - 5)
            elif pressed & buttons.BOTTOM_RIGHT != 0:
                self._time_val += 5
            elif pressed & buttons.TOP_RIGHT != 0:
                return Alarm(self._time_val)


while True:
    SetupMenu().start_alarm().wait()
    utime.sleep(0.25)
