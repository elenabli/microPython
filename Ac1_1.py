from machine import Pin, Timer
import time

led1 = Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(22, Pin.OUT)
leds = (led1, led2, led3)

while True:
    for led in leds:
        led.on()
        
        time.sleep(1)
        led.off()