import numpy as np
import matplotlib.pyplot as plt

l =np.array([671.6,623.4,579.1,577.0,546.1,496.0,491.6,435.8,407.8,404.7])

Dm = np.array([61.58,62.27,62.93,62.97,63.60,64.87,64.97,67.38,69.27,69.48])

plt.plot(l,Dm,'+')
plt.plot()
plt.show()

n = np.sin(np.pi*(Dm+60)/(2*180)) / np.sin(np.pi*30/180)

l_2 = 1/l**2

plt.plot(l_2,n,'+',color='red')
plt.grid()

P=np.polyfit(l_2, n , 1)

A= P[0] # A
B= P[1] # B


plt.plot(l_2,A*l_2 + B)

plt.show()