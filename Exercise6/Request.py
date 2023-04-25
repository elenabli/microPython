import network
from time import sleep
from machine import I2C, Pin
import ssd1306
import urequests as requests


def connection():
    ssid = 'peace and love'
    psw = 'carrot-cake-with-cinammon'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psw)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        oled.fill(0)
        oled.text('Wait', 0, 0, 1)
        oled.show()
        sleep(1)
    ip = wlan.ifconfig()[0]
    print('Connected on ' + ip)
    oled.fill(0)
    oled.text(ip, 0, 0, 1)
    oled.show()
    return ip
 

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

try:
    ip = connection()
    response = requests.get('http://192.168.50.3:8000')
    if response.status_code == 200:
        print('response received')
#         oled.fill(0)
        oled.text('response received', 0, 15, 1)
        oled.show()
except KeyboardInterrupt:
    machine.reset()