import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 





file_name="121217-011818Lin.csv"
file_path="./Test/UnifNoise1.0/"+file_name
Returns_in = pd.read_csv(file_path,delimiter=" ")
print(len(Returns_in))

ob_ret=(Returns_in["Returns"])


PortValue=[]

PortValue.append(100000)

for x in range(0,25):
	PortValue.append(PortValue[x]*(1+ob_ret[x]))

print(PortValue[25])

# # Data for plotting
# t = np.arange(0, 26, 1)
# ##Change to returns to get returns vs time
# s = PortValue

# fig, ax = plt.subplots()
# ax.plot(t, s)

# ax.set(xlabel='time (days)', ylabel='Portfolio Value',
#        title='Portfolio Value VS Time')
# ax.grid()

# fig.savefig("UnifNoise8.png")
