from machine import Pin, I2C
import math
import ssd1306
from time import sleep

# Mean PPI
# mean heart rate (HR)
# Standard deviation of PPI (SDNN)
# Root mean square of successive differences (RMSSD)

ppi1 = [1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100]
ppi2 = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]
ppi = [ppi1, ppi2]

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

for n in ppi:
    mean_ppi = round(sum(n)/len(n))
    mean_hr = round(60/(mean_ppi/1000))
    sdnn = round(math.sqrt(sum([(i-mean_ppi)**2 for i in n])/(len(n)-1)))
    rmssd = round(math.sqrt(sum([(n[i+1] - n[i])**2 for i in range(len(n)-1)])/(len(n)-1)))
    print('mean PPI = ' + str(mean_ppi) + 'ms\n'
          'mean HR = ' + str(mean_hr) + 'ms\n'
          'SDNN = ' + str(sdnn) + 'ms\n'
          'RMSSD = ' + str(rmssd) + 'ms\n')
    oled.fill(0)
    oled.text('mean PPI = ' + str(mean_ppi) + 'ms', 0, 0, 1)
    oled.text('mean HR = ' + str(mean_hr) + 'ms', 0, 15, 1)
    oled.text('SDNN = ' + str(sdnn) + 'ms', 0, 30, 1)
    oled.text('RMSSD = ' + str(rmssd) + 'ms', 0, 45, 1)
    oled.show()
    sleep(5)
    

