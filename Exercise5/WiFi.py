import network
# import socket
from time import sleep
# from picozero import pico_temp_sensor, pico_led
from machine import I2C, Pin
import ssd1306


ssid = 'KME670Group8'
psw = 'or2i2hA00HVJsa1xMiIs'

def connection():
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
except KeyboardInterrupt:
    machine.reset()
