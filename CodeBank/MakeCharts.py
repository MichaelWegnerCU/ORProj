import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 





file_name="071818-092718.csv"
file_path="../Data/Test/Noise3.0/"+file_name
Returns_in = pd.read_csv(file_path,delimiter=" ")
print(len(Returns_in))

ob_ret=(Returns_in["Returns"])


PortValue=[]

PortValue.append(100000)

for x in range(0,50):
	PortValue.append(PortValue[x]*(1+ob_ret[x]))

# Data for plotting
t = np.arange(0, 51, 1)
##Change to returns to get returns vs time
s = PortValue

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (days)', ylabel='Portfolio Value',
       title='Portfolio Value VS Time')
ax.grid()

fig.savefig("Noise3_PortValue_vs_time_50.png")
