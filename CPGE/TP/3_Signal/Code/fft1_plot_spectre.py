import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

# Use LaTeX for text rendering
rc('text', usetex=True)
rc('font', family='serif')

""" ÉCHANTILLONNAGE """
f0 = 200
fe = 1000
T  = 0.1
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

from numpy.fft import fft

""" SPECTRE EN FRÉQUENCE """
TF = np.abs(fft(s))
f  = np.linspace(0,fe,int(fe*T))
plt.xlabel(r'$f$')
plt.ylabel(r'amplitude')
plt.plot(f,TF,'b')
plt.savefig('spectre_fe={}.pdf'.format(fe))
plt.show()
