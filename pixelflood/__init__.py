import ugfx
import wifi
import usocket
import _thread
from time import sleep


def clear_screen():
    for color in [ugfx.WHITE, ugfx.BLACK, ugfx.WHITE]:
        ugfx.clear(color)
        ugfx.flush()


def socket_create(port):
    sock = usocket.socket()
    addr_info = usocket.getaddrinfo("0.0.0.0", port)
    addr = addr_info[0][-1]
    sock.bind(addr)
    sock.listen(23)
    return sock


def pixelflood_server(sock):
    while True:
        client_sock = sock.accept()[0]
        _thread.start_new_thread(pixelflood_handler, (client_sock,))

def pixelflood_handler(client_sock):
    while True:
        line = client_sock.readline().decode('ascii')
        if line == '' or line == '\r\n':
            break
        
        line_parts = line.split(' ')
        if len(line_parts) != 4  or line_parts[0] != 'PX':
            break
        
        try:
            int(line_parts[1])
            int(line_parts[2])
            int(line_parts[3], 16)
        except ValueError:
            break
        
        x, y = int(line_parts[1]), int(line_parts[2])
        col  = ugfx.BLACK if int(line_parts[3], 16) < 0x800000 else ugfx.WHITE
        
        if x in range (0, 296) and y in range(0, 128):
            ugfx.pixel(x, y, col)
            ugfx.flush()

    client_sock.close()


ugfx.init()
wifi.init()

# connect to wifi
clear_screen()
ugfx.string(0, 0, 'Connecting to Wifi..', 'Roboto_Regular12', ugfx.BLACK)
ugfx.flush()
while not wifi.sta_if.isconnected():
    sleep(0.1)
    pass
current_ip = wifi.sta_if.ifconfig()[0]
ugfx.string(0, 14, 'Starting server on %s:2323' % (current_ip), 'Roboto_Regular12', ugfx.BLACK)
ugfx.flush()

# start server
try:
    sock = socket_create(2323)
    pixelflood_server(sock)
except OSError:
    clear_screen()
    ugfx.string(0, 0, 'An OSError occured. Duno.', 'Roboto_Regular12', ugfx.BLACK)
except:
    clear_screen()
    ugfx.string(0, 0, 'Something failed \_(;_;)_/', 'Roboto_Regular12', ugfx.BLACK)
ugfx.flush()

while True:
    pass
