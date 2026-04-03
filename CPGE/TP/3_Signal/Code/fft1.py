import numpy as np
import matplotlib.pyplot as plt

""" ÉCHANTILLONNAGE """
f0 = 200
fe = 10000
T  = 0.01
N  = int(T*fe)
t  = np.linspace(0,T,N)
s  = np.cos(2*np.pi*f0*t)

""" VARIATION DANS LE TEMPS """
plt.xlim(0,T)
plt.ylim(-1.5,1.5)
plt.xlabel('t')
plt.ylabel('s(t)')
plt.plot(t,s,'b+-')        
plt.show()
