import network
from time import sleep
from machine import I2C, Pin
import ssd1306
import urequests as requests
import ujson


def connection():
    ssid = 'KME670Group8'
    psw = 'or2i2hA00HVJsa1xMiIs'
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

APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800] #Interval data to be sent to KuniosCloud

data_set = {
  "type": "RRI",
  "data": intervals,
  "analysis": {
    "type": "readiness"}
}

try:
    ip = connection()
    
    #get token
    response = requests.post(
        url = TOKEN_URL,
        data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
        headers = {'Content-Type':'application/x-www-form-urlencoded'},
        auth = (CLIENT_ID, CLIENT_SECRET))

    response = response.json() 
    access_token = response["access_token"]
    
    #get data analysis
    response = requests.post(
        url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
        headers = { "Authorization": "Bearer {}".format(access_token), 
        "X-Api-Key": APIKEY },
        json = data_set)
    
    response = response.json()
    print(response)
    print(response['analysis']['pns_index'], response['analysis']['sns_index'])
    oled.fill(0)
    oled.text('pns: ' + str(response['analysis']['pns_index']), 0, 0, 1)
    oled.text('sns: ' + str(response['analysis']['sns_index']), 0, 15, 1)
    oled.show()
except KeyboardInterrupt:
    machine.reset()
