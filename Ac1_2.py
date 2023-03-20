
from machine import Pin
import time

led1 = Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(20, Pin.OUT)

while True:
    for i in range(8):
        state = bin(i)[2:]
        if len(state)<3:
            state = "0" * (3 - len(state)) + state    
        print(state)
        led1.on() if state[2] == '1' else led1.off()
        led2.on() if state[1] == '1' else led2.off()
        led3.on() if state[0] == '1' else led3.off()
        time.sleep(1)
        
        