import display
import interrupt
import utime
import vibra

def show_display(i):
    with display.open() as disp:
        disp.clear()
        disp.print("{}".format(i))
        disp.update()
        disp.close()

def alarm_fun(x):
    show_display("0w0")
    vibra.vibrate(200)

interrupt.set_callback(interrupt.RTC_ALARM, alarm_fun)
interrupt.enable_callback(interrupt.RTC_ALARM)

utime.alarm(utime.time() + 5)

show_display("gumo, t-5")

while True:
    pass
