from machine import Pin, PWM, I2C
import ssd1306
import time
# import _thread

rota = Pin (10, Pin.IN, Pin.PULL_UP)
rotb = Pin (11, Pin.IN, Pin.PULL_UP)
rotbtn = Pin(12, Pin.IN, Pin.PULL_UP)

led1 = PWM(Pin(22, Pin.OUT))
led2 = PWM(Pin(21, Pin.OUT))
led3 = PWM(Pin(20, Pin.OUT))

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initial mode - LED selection
mode = False
debounce_time = 0
select_led = 0
selected_led = 1

#Initial brightness
brights = [0,0,0]

def encoder_rotation(pin):
    global  mode, select_led, selected_led
    if mode == False:
        if rotb.value() == 1:
            select_led -= 10
            if select_led <= 1:
                select_led = 1             
        else:
            select_led += 10
            if select_led >= 90:
                select_led = 90

        if 0 <= select_led <= 30:
            selected_led = 1

        elif 30 < select_led <= 60:
            selected_led = 2

        else:
            selected_led = 3

    else:
        # mode: brightness
        index = selected_led-1
        bright1=brights[index]
        if rotb.value() == 1:
            bright1 -= 5
            if bright1 <= 0:
                bright1 = 0 

        else: 
            bright1 += 5
            if bright1 >= 100:
                bright1 = 100 

        brights[index] = bright1
    
def switch_mode(pin):
    global mode, debounce_time
    if (time.ticks_ms()-debounce_time) > 300:
        mode = not mode
        debounce_time=time.ticks_ms()
    

def display():
#     while True:
        oled.fill(0)
        oled.text('Mode: LED select', 0, 0, 1)
        text = "LED "+ str(selected_led)
        oled.text(text, 0, 15, 1)
        
        if mode:
            bar_length = int(brights[selected_led-1] * 15 / 100)
            bar = '|' * bar_length#+ " " * (15 - bar_length)
                    
            oled.fill(0)
            oled.text('Mode: brightness', 0, 0, 1)
            oled.text(text, 0, 15, 1)
            oled.text(str(brights[selected_led-1]) + '%', 0, 30, 1)
            oled.text(bar, 0, 45, 1)
            
        oled.show()
    
    
rota.irq(handler=encoder_rotation, trigger=Pin.IRQ_RISING)

rotbtn.irq(handler=switch_mode, trigger=Pin.IRQ_FALLING)

# _thread.start_new_thread(display, ())

while True:
    display()
    led1.duty_u16(int(brights[0]/100 * 65534))
    led2.duty_u16(int(brights[1]/100 * 65534))
    led3.duty_u16(int(brights[2]/100 * 65534))
    

