import numpy as np
import matplotlib.pyplot as plt

""" PARAMÈTRES PHYSIQUES """
Omega = 2*np.pi/10 # vitesse angulaire de rotation du plateau
v0    = ...        # vitesse initiale

""" PARAMÈTRES PROGRAMME """
N    = 1000   # nombre de points de tracé
tmax = 0.5    # temps maximal de tracé
t    = ...    # tableau comprenant N instants régulièrement espacés de 0 à tmax

""" TRACÉ """
x = v0*t*np.cos(Omega*t)  # abscisse
y = ...                                                             # ordonnée

plt.xlim(-1,1)  # interalle des x sur le graphe
plt.ylim(-1,1)  # interalle des y sur le graphe

plt.xlabel('x') # étiquette axe x
plt.ylabel('y') # étiquette axe y

plt.plot(x,y)   # tracé des équations horaires
plt.show()      # affichage de la figure
