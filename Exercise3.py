from machine import ADC
from piotimer import Piotimer
from fifo import Fifo

sensor = ADC(26)
fifo = Fifo(150)

read_frequency = 250
# for filtering:
# how many values to take to calculate the average (for smoothing) 
sampling_count = 5
# interval between values read from the sensor
interval_ms = (1000 / read_frequency)
# interval between values in the filtered list
sampled_interval_ms = interval_ms * sampling_count
# how many values should be in the list to calculate the rhythm
hr_sample_range_count = 2000 / sampled_interval_ms


# Function called by the timer reads data from the sensor
def read_adc_value(tmr):
    sensor_value = sensor.read_u16()
    fifo.put(sensor_value)
    

timer = Piotimer(freq=read_frequency, mode=Piotimer.PERIODIC, callback=read_adc_value)

# The main function that reads data from the list, finds peaks and calculates the heart rate
def hr_from_sample(samplings):
    threshold = 1.009* (sum(samplings)/len(samplings))

    maxi = 0
    current_peak_index = 0
    previous_peak_index = 0
    heart_rates_in_samples = []
    
    for i in range(len(samplings)):        
        sample = samplings[i]
        # compare value with threshold and store index of peak
        if sample > threshold:
            if sample > maxi:
                maxi = sample
                current_peak_index = i
                
        # find the interval between peaks
        else:
            maxi = 0
            diff = current_peak_index - previous_peak_index
            ppi = diff * sampled_interval_ms
            
            # if the value of the interval is within the set range, calculate the pulse
            if 250 < ppi < 1000:

                hr = 60/(ppi/1000)
                print(hr)
                heart_rates_in_samples.append(hr)   # store heart rate's value in the list
                previous_peak_index = current_peak_index 
           
    return heart_rates_in_samples[1:]  # remove the first value as it might be wrong

raw_values = [] 
filtered_values = [] 
hr_list = [80] 

while True:

    if not fifo.empty():
        val = fifo.get()
        raw_values.append(val)   
        # filter the signal: take a certain number of values and calculate the average 
        if len(raw_values) == sampling_count:
            avg = sum(raw_values)/len(raw_values)
            filtered_values.append(avg)
            
            raw_values = [] 
            
        # calculate the heart rate in 2 seconds interval
        if len(filtered_values) == hr_sample_range_count:
            hr_from_2_sec = hr_from_sample(filtered_values)   # call the main function
            hr_list= hr_list + hr_from_2_sec
            hr_list = hr_list[-5:]   # take only 5 last values

            print(hr_list)
            filtered_values=[]
            avg_hr = str(int(sum(hr_list)/len(hr_list)))
            
            print('Heart rate: '+ avg_hr + ' bmp')






            
        