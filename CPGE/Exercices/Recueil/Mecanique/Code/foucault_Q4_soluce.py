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
omega   = np.sqrt(Omega**2*np.sin(lat)**2 + omega0**2)     # pulsation rotation du plan

""" PARAMÈTRES NUMERIQUES """

N    = 10	 	# nombre de périodes de tracé
x0   = 0.5 		# conditions initiales avec vy0 = 0
tmax = N*T0		# temps maximale de tracé
t    = np.linspace(0,tmax,100*N) # tableau des dates de tracé

""" TRACÉ """

x = +x0*np.cos(Omega**np.sin(lat)*t)*np.cos(omega*t)
y = -x0*np.sin(Omega**np.sin(lat)*t)*np.cos(omega*t)

plt.figure()
plt.xlim(-1.5*x0,1.5*x0)
plt.ylim(-1.5*x0,1.5*x0)
plt.xlabel('x')
plt.ylabel('y')
plt.plot(x,y)
plt.show()
