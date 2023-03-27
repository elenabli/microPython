from machine import Pin, I2C
import ssd1306

sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
rotary_button = Pin(12, Pin.IN, Pin.PULL_UP)
led1 = Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(20, Pin.OUT)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

state_sw0 = False
state_sw1 = False
state_sw2 = False

def handler (pin):
    led1.off()
    led2.off()
    led3.off()
    
rotary_button.irq(handler=handler, trigger=Pin.IRQ_FALLING)

while True:
    sw0_pressed = not sw0.value()
    sw1_pressed = not sw1.value()
    sw2_pressed = not sw2.value()
    
    if sw0_pressed and not state_sw0:
        led1.toggle()
    if sw1_pressed and not state_sw1:
        led2.toggle()
    if sw2_pressed and not state_sw2:
        led3.toggle()
        
    state_sw0 = sw0_pressed
    state_sw1 = sw1_pressed
    state_sw2 = sw2_pressed
    
    oled.fill(0)
    
    oled.text("LED1: "+ str(led1.value()), 0, 0, 1)
    oled.text("LED2: "+ str(led2.value()), 0, 15, 1)
    oled.text("LED3: "+ str(led3.value()), 0, 30, 1)
    
    oled.show()

