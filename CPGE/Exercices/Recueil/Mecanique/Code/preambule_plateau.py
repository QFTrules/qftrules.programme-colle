import numpy as np
import matplotlib.pyplot as plt

""" PARAMÈTRES PHYSIQUES """
Omega = 2*np.pi/10 # vitesse angulaire de rotation du plateau
v0    = ...        # À MODIFIER

""" PARAMÈTRES PROGRAMME """
N    = 1000   # nombre de points de tracé
tmax = 0.5    # temps maximal de tracé
t    = ...    # À MODIFIER 

""" TRACÉ """
x = v0*t*np.cos(Omega*t)  # abscisse
y = ...                   # À MODIFIER

plt.figure()    # création d'une figure
plt.xlim(-1,1)  # interalle des x sur le graphe
plt.ylim(-1,1)  # interalle des y sur le graphe

plt.xlabel('x') # étiquette axe x
plt.ylabel('y') # étiquette axe y

plt.plot(x,y)   # tracé des équations horaires
plt.show()      # affichage de la figure
