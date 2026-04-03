

import numpy as np

import matplotlib.pyplot as plt

lo = 6e-7  # longueur d'onde du système interférométrique
D = 2.5e-13

epsilon = np.linspace(.5, 5, 5)
i = lo/epsilon/np.pi*180
q = 2*np.pi/i

donnees = np.load("2041JKPA.npy")  # chargement des données expérimentales
# exemple d'utilisation des données. ces données contiennent 5 expériences correspondant aux 5 valeur de epsilon.
# le premier tableau contient les valeurs de t et le second les valeurs de g(t)
t = donnees[0, 0, :]
g = donnees[0, 1, :]

# ici on trace les valeurs pour le premier set de données j=0

plt.plot(t, g)
plt.xlabel(r'$t$')
plt.ylabel(r'$g(t)$')
plt.show()
