import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

# Use LaTeX for text rendering
rc('text', usetex=True)
rc('font', family='serif')

""" ÉCHANTILLONNAGE """
f0 = 200
fe = 3000
T  = 0.01
N  = int(T*fe)
t  = np.linspace(0,T,N)
s  = np.cos(2*np.pi*f0*t)

""" VARIATION DANS LE TEMPS """
plt.xlim(0,T)
plt.ylim(-1.5,1.5)
plt.xlabel(r't')
plt.ylabel(r's(t)')
plt.plot(t,s,'b+-')        
plt.savefig('fe={}.pdf'.format(fe))
plt.show()
