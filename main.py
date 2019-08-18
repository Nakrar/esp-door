# upip.install('micropython-logging')
import socket
import time

from machine import Pin

print('load test')

import wifi

print('do wifi.disable_ap')
wifi.disable_ap()
wifi.do_connect()


def main():
    print('load main')
    last_state = 0
    # 0 for connection, 1 for no connection
    p5 = Pin(5, Pin.IN, Pin.PULL_UP)

    while True:
        door_open = p5.value()
        print('read pin value:, ', door_open)
        if last_state != door_open:
            if door_open:
                get_time()
            last_state = door_open

            print('pin change', door_open)

        time.sleep_ms(500)


def get_time():
    print('get_time')
    # http://worldtimeapi.org/api/timezone/Asia/Tokyo

    data = http_get("http://worldtimeapi.org/api/timezone/Asia/Tokyo")
    date = str(data, 'utf8')

    # get datetime from it
    # . . . 9:00","utc_datetime":"2019-06-17T11:59:57.333119+00:00","un . . .

    utc_start = date.find('datetime')
    time_start = date.find('T', utc_start)
    hour_end = date.find(':', time_start)

    hour = int(data[time_start + 1: hour_end], 10)
    # timezone
    hour += 9
    hour %= 24

    if hour > 18:
        http_get("http://192.168.0.13/strip/wall?value=100")
        time.sleep(0.3)
        http_get("http://192.168.0.13/strip/window?value=100")
        print('get_time on led')


def http_get(url):
    print('http_get', url)

    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

    s.settimeout(1)

    data = b''

    try:
        while True:
            packet = s.recv(512)
            if not packet:
                break
            data += packet
    except OSError:
        return

    s.close()

    print('http_get data', data)

    return data


main()
