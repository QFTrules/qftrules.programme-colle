import numpy as np
import matplotlib.pyplot as plt

""" PARAMÈTRES PHYSIQUES """

g       = 9.81            # accélération de la pesanteur
lat     = 45/180*np.pi    # latitude à Paris
L       = 3               # longueur du pendule

Tsid    = 100             # durée du jour sidéral
Omega   = 2*np.pi/Tsid    # vitesse angulaire de rotation terrestre
omega0  = np.sqrt(g/L)    # pulsation propre du pendule
T0      = 2*np.pi/omega0  # période propre du pendule
omega   = ...             # À MODIFIER

""" PARAMÈTRES NUMERIQUES """

tmax = 10*T0    # temps maximale de tracé
t    = np.linspace(0,tmax,1000) # tableau des dates de tracé

""" TRACÉ """

x0  = 0.5 # conditions initiales avec vy0 = 0
x   = ... # À MODIFIER
y   = ... # À MODIFIER

plt.figure()
plt.xlim(-1.5*x0,1.5*x0)
plt.ylim(-1.5*x0,1.5*x0)
plt.xlabel('x')
plt.ylabel('y')
plt.plot(x,y)
plt.show()
