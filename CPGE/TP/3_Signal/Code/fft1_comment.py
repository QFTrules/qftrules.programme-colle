import numpy as np
import matplotlib.pyplot as plt

""" ÉCHANTILLONNAGE """
f0 = 200                            # fréquence du signal (Hz)
fe = 10000                          # fréquence d'échantillonnage (Hz)
T  = 0.01                           # durée d'acquisistion (s)
N  = int(T*fe)                      # nombre de points
t  = np.linspace(0,T,N)             # instants d'échantillonnage
s  = np.cos(2*np.pi*f0*t)           # signal sinusoïdal échantillonné

""" VARIATION DANS LE TEMPS """
plt.xlim(0,T)               # intervalle des abscisses
plt.ylim(-1.5,1.5)          # intervalle des ordonnées
plt.xlabel('t')             # étiquette abscisse
plt.ylabel('s(t)')          # étiquette ordonnées
plt.plot(t,s,'b+-')         # tracé en croix (+) reliées (-) bleues (b)
plt.show()                  # affichage figure
