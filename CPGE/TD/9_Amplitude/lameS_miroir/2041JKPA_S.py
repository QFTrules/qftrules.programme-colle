

import numpy as np

import matplotlib.pyplot as plt

lo = 6e-7  # longueur d'onde du système interférométriqu
lmin = 6.5e-6
lmax = 65e-6
D = 2.5e-13

epsilon = np.linspace(.5, 5, 5)
i = lo/epsilon/np.pi*180
q = 2*np.pi/i

donnees = np.load("2041JKPA.npy")
tauinv = np.zeros(5)
for j in range(5):

    tauinv[j], b = np.polyfit(donnees[j, 0, :], np.log(donnees[j, 1, :]), 1)


plt.plot(q**2, tauinv)
plt.xlabel(r'$q^2$ en $m^{-2}$')
plt.ylabel(r'$\dfrac{1}{\tau}$ en $s^{-1}$')
plt.show()

D, b = np.polyfit(q**2, tauinv, 1)
print('D={0:2.1e} m/s^2'.format(D))
