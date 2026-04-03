import numpy as np
import matplotlib.pyplot as plt

""" PARAMÈTRES PHYSIQUES """
Omega = 2*np.pi/10 # vecteur rotation terrestre
d     = 1          # position initiale

""" PARAMÈTRES PROGRAMME """
N    = 1000                     # nombre de points de tracé
tmax = 40		                # temps maximal de tracé
t    = np.linspace(0,tmax,N)    # tableau des dates de tracé

""" TRACÉ """
x = -d*np.cos(Omega*t)*np.cos(np.sqrt(2)*Omega*t) - d/np.sqrt(2)*np.sin(Omega*t)*np.sin(np.sqrt(2)*Omega*t)
y = -d*np.sin(Omega*t)*np.cos(np.sqrt(2)*Omega*t) + d/np.sqrt(2)*np.cos(Omega*t)*np.sin(np.sqrt(2)*Omega*t)
plt.xlim(-1.5*d,1.5*d)
plt.ylim(-1.5*d,1.5*d)
plt.xlabel('x')
plt.ylabel('y')
plt.plot(x,y)
plt.show()
