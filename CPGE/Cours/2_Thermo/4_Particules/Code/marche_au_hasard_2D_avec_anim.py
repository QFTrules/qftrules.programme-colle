# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 16:13:56 2021

@author: JM Biansan
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation





#à 2D
libre_parcours=1
tau=1
nbe_pas=100
nbe_particules=1000
#initialisation des <r²>, des abscisses x, des ordonnées y et des dates
r2moyen=np.zeros(nbe_pas)
dates=np.zeros(nbe_pas)
x=np.zeros(nbe_particules)
y=np.zeros(nbe_particules)
#les xx et yy stockent dans un tableau 2D les coordonnées aux différentes dates; xx et yy ne servent plus tard que pour l'animation, ils sont inutiles au tracé de <r²> en fonction de t
xx,yy=np.zeros((nbe_pas,nbe_particules)),np.zeros((nbe_pas,nbe_particules))


for i in range(nbe_pas):
    #on tire aléatoirement l'angle polaire du vecteur déplacement
    theta=np.random.uniform(0,2*np.pi,nbe_particules)
    x=x+np.cos(theta)*libre_parcours
    y=y+np.sin(theta)*libre_parcours
    xx[i]=x
    yy[i]=y
    #calcul tableau des r²
    r2=np.square(x)+np.square(y)
    r2moyen[i]=np.sum(r2)/nbe_particules
    dates[i]=i*tau

plt.figure(1)
plt.plot(dates,r2moyen,label='Simulation')
plt.plot(dates,dates*libre_parcours**2/tau,label='Théorie')
plt.grid()
plt.legend()
plt.xlabel('t')
plt.ylabel('<r²>')
plt.title('Marche au hasard à deux dimensions: <r²>=f(t)')




#animation de la diffusion 2D
fig = plt.figure(2) # initialise la figure
plt.xlabel('x')
plt.xlabel('y')
plt.title('Diffusion à 2D')
line, = plt.plot([],[],'.',markersize=1)
plt.xlim(-3*np.sqrt(nbe_pas*libre_parcours**2), 3*np.sqrt(nbe_pas*libre_parcours**2))
plt.ylim(-3*np.sqrt(nbe_pas*libre_parcours**2),3*np.sqrt(nbe_pas*libre_parcours**2))


def init():
    line.set_data([],[])
    return line,

def animate(i):
    line.set_data(xx[i], yy[i])
    return line,


ani = animation.FuncAnimation(fig, animate, init_func=init, frames=nbe_pas, blit=True, interval=200, repeat=False)


plt.show()





