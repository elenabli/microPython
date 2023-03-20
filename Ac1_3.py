
from machine import Pin, PWM
import time

led1 = PWM(Pin(22))
led2 = PWM(Pin(21))
led3 = PWM(Pin(20, Pin.OUT))

# def fadeOn(l):
#     for i in range(0,20000):
#         l.duty_u16(i)
#         time.sleep(0.0001)
# 
# def fadeOff(l):
#         for i in range(20000,0, -1):
#             l.duty_u16(i)
#             time.sleep(0.0001)
        
while True:
    for i in range(8):
        state = bin(i)[2:]
        if len(state)<3:
            state = "0" * (3 - len(state)) + state    
        print(state)
        
        for i in range(0,10000):
            if state[2] == '1':
                led1.duty_u16(i)
            if state[1] == '1':
                led2.duty_u16(i)
            if state[0] == '1':
                led3.duty_u16(i)
            time.sleep(0.00001)
            
        for i in range(10000,0,-1):
            if state[2] == '1':
                led1.duty_u16(i)
            if state[1] == '1':
                led2.duty_u16(i)
            if state[0] == '1':
                led3.duty_u16(i)
            time.sleep(0.00001)

        time.sleep(1)