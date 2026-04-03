#!/usr/bin/env python
## Données exportées de Pymecavidéo
## 20/06/23 14:14

import numpy as np
import matplotlib.pyplot as plt

# Intervalle de temps auto-détecté
dt=0.03333333333333333

# coordonnées du point numéro 1
x1 = np.array([-382.0, -369.0, -355.0, -341.0, -330.0, -318.0, -306.0, -293.0, -281.0, -269.0, -256.0, -244.0, -232.0, -219.0, -206.0, -194.0, -182.0, -169.0, -157.0, -144.0, -132.0, -120.0, -107.0, -95.0, -83.0, -70.0, -58.0, -45.0, -33.0, -19.0, -8.0, 5.0, 17.0, 30.0, 42.0, 55.0, 67.0, 80.0, 93.0, 106.0, 120.0, 132.0, 145.0, 157.0, 170.0, 183.0, 196.0, 209.0, 222.0, 235.0, 248.0, 262.0, 275.0, 288.0, 301.0, 314.0, 341.0, 353.0, 367.0, 380.0, 394.0, 407.0, 420.0, 434.0, 446.0, 460.0, 473.0, 486.0, 499.0, 513.0, 527.0, 540.0, 553.0, 566.0, 579.0, 593.0, 606.0, 619.0, 632.0, 646.0, 660.0, ])
y1 = np.array([-45.0, -44.0, -42.0, -41.0, -40.0, -39.0, -37.0, -36.0, -35.0, -34.0, -33.0, -31.0, -31.0, -29.0, -28.0, -27.0, -26.0, -24.0, -23.0, -22.0, -20.0, -19.0, -18.0, -17.0, -16.0, -15.0, -13.0, -12.0, -11.0, -9.0, -9.0, -7.0, -6.0, -5.0, -4.0, -2.0, -1.0, 0, 2.0, 3.0, 5.0, 5.0, 7.0, 7.0, 9.0, 10.0, 11.0, 13.0, 14.0, 16.0, 17.0, 19.0, 19.0, 21.0, 22.0, 23.0, 26.0, 27.0, 28.0, 30.0, 31.0, 32.0, 34.0, 35.0, 36.0, 37.0, 39.0, 40.0, 42.0, 43.0, 45.0, 46.0, 47.0, 48.0, 50.0, 51.0, 52.0, 54.0, 55.0, 57.0, 58.0, ])

##############################################################
# Le code auto-généré qui suit peut être effacé à volonté.   #
##############################################################
# Il n'est là qu'à titre d'exemple, et il n'est pas toujours #
# approprié à l'usage des données que vous avez exportées.   #
##############################################################

## affichage des points
plt.plot(x1,y1,'o',markersize= 3)
plt.xlabel("x (en m)")
plt.ylabel("y (en m)")

## calcul et affichage des vecteurs vitesses




Δt = 2*dt
vx = np.array(np.zeros(len(x1)-2))
vy = np.array(np.zeros(len(x1)-2))
i=0
for k in range(1,len(x1)-1):
    Δx = (x1[k+1]-x1[k-1])
    Δy = (y1[k+1]-y1[k-1])
    vx[i] = Δx/Δt
    vy[i] = Δy/Δt
    i+=1

plt.quiver(x1[1:-1], y1[1:-1], vx, vy, scale_units = 'xy', angles = 'xy', width = 0.003)
 

## calcul et affichage des vecteurs accélérations


ax = np.array(np.zeros(len(vx)-2))
ay = np.array(np.zeros(len(vx)-2))
i=0
for k in range(1, len(vx)-1):
    Δvx = (vx[k+1]-vx[k-1])
    Δvy = (vy[k+1]-vy[k-1])
    ax[i] = Δvx/Δt
    ay[i] = Δvy/Δt
    i+=1

plt.title("Vecteurs accélérations") 
plt.quiver(x1[2:-2], y1[2:-2], ax, ay, scale_units = 'xy', angles = 'xy', width = 0.003, color = 'r')

## présentation du diagramme interactif
plt.grid()
plt.show()
