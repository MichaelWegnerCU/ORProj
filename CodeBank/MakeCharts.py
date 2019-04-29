import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 





file_name="121217-127617.csv"
file_path="../Data/Test/"+file_name
Returns_in = pd.read_csv(file_path,delimiter=" ")

ob_ret=(Returns_in["Returns"])


PortValue=[]

PortValue.append(100000)

for x in range(0,9):
	print(x)
	PortValue.append(PortValue[x]*(1+ob_ret[x]))

# Data for plotting
t = np.arange(0, 10, 1)
##Change to returns to get returns vs time
s = ob_ret

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (days)', ylabel='Returns',
       title='Returns VS Time')
ax.grid()

fig.savefig("Returnsover10days.png")
