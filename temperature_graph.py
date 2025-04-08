# sudo apt-get install python3-matplotlib

import os
import time
import matplotlib.pyplot as plt

def get_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return float(temp.replace("temp=", "").replace("'C\n", ""))

temps = []
times = []

for i in range(60):  # Collect data for 60 seconds
    temps.append(get_temp())
    times.append(i)
    time.sleep(1)

plt.plot(times, temps)
plt.xlabel('Time (seconds)')
plt.ylabel('Temperature (°C)')
plt.title('Raspberry Pi CPU Temperature Over Time')
plt.show()
