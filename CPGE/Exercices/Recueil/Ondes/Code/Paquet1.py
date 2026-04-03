import numpy as np
N    = 2**12     # Nombre de valeurs de k et de x
xmin = -10       # valeur minimale de x
xmax = 10        # valeur maximale de x
L    = xmax-xmin # Longueur de l'intervalle
X    = np.linspace(xmin, xmax, N)   # tableau des x
k    = np.linspace(0,2*np.pi*N/L,N) # tableau des k

k0     = 6
deltak = 1
A      = ...
