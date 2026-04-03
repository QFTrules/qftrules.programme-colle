	import numpy as np
import matplotlib.pyplot as plt

""" PARAMÈTRES PHYSIQUES """
g     = 9.81			# accélération de la pesanteur
Tsid  = 100				# jour sidéral
Omega = 2*np.pi/Tsid	# vecteur rotation terrestre
lat	  = 45/180*np.pi	# latitude
L     = 3				# longueur du pendule

a	    = Omega*np.sin(lat)				# pulsation auxiliaire		
omega0  = np.sqrt(g/L)					# pulsation du pendule
T0	    = 2*np.pi/omega0				# pulsation du pendule
omega   = np.sqrt(a**2 + omega0**2)		# pulsation rotation du plan
T       = 2*np.pi/omega					# période rotation du plan

""" PARAMÈTRES PROGRAMME """

N    = 10	 	# nombre de périodes de tracé
x0   = 0.5 		# conditions initiales avec vy0 = 0
tmax = N*T0		# temps maximale de tracé
t    = np.linspace(0,tmax,100*N) # tableau des dates de tracé

""" TRACÉ """
x = +x0*np.cos(a*t)*np.cos(omega*t) + a*x0/omega*np.sin(a*t)*np.sin(omega*t)
y = -x0*np.sin(a*t)*np.cos(omega*t) + a*x0/omega*np.cos(a*t)*np.sin(omega*t)
plt.xlim(-1.5*x0,1.5*x0)
plt.xlim(-1.5*x0,1.5*x0)
plt.xlabel('x')
plt.ylabel('y')
plt.plot(x,y)
plt.show()
