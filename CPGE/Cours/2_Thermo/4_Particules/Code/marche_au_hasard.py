# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 16:13:56 2021

@author: JM Biansan
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#à 1D
libre_parcours=1
tau=1
nbe_pas=100
nbe_particules=10000

#initialisation des <r²>, des abscisses x et des dates
r2moyen=np.zeros(nbe_pas)
dates=np.zeros(nbe_pas)
x=np.zeros(nbe_particules)

for i in range(nbe_pas):
        #random.choice(np.array([-1,1]) renvoie -1 ou 1
        #on tire autant de valeurs de ce type qu'il y a de particules et on le stocke dans "sens"
    sens=np.random.choice(np.array([-1,1]),nbe_particules)
    #sens=-1+2*np.random.randint(0,2,nbe_particules)
        #on augmente x de chaque particule d'un libre parcours moyen à gauche ou à droite avec une égale probabilité
        #l'opération est faite directement sur le tableau numpy pour aller plus vite
    x=x+sens*libre_parcours
    #calcul du tableau des x²
    x2=np.square(x)
    #calcul de <r²>
    r2moyen[i]=np.sum(x2)/nbe_particules
    dates[i]=i*tau

plt.figure(0)
plt.plot(dates,r2moyen,label='Simulation')
plt.plot(dates,dates*libre_parcours**2/tau,label='Théorie')
plt.grid()
plt.legend()
plt.xlabel('t')
plt.ylabel('<r²>')
plt.title('Marche au hasard à une dimension: <r²>=f(t)')


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



for i in range(nbe_pas):
    #on tire aléatoirement l'angle polaire du vecteur déplacement
    theta=np.random.uniform(0,2*np.pi,nbe_particules)
    x=x+np.cos(theta)*libre_parcours
    y=y+np.sin(theta)*libre_parcours

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

#à 3D
libre_parcours=1
tau=1
nbe_pas=100
nbe_particules=1000
r2moyen=np.zeros(nbe_pas)
dates=np.zeros(nbe_pas)
x=np.zeros(nbe_particules)
y=np.zeros(nbe_particules)
z=np.zeros(nbe_particules)

for i in range(nbe_pas):
    #on tire aléatoirement theta et phi du vecteur déplacement
    theta=np.random.uniform(0,np.pi,nbe_particules)
    phi=np.random.uniform(0,2*np.pi,nbe_particules)
    x=x+np.sin(theta)*np.cos(phi)*libre_parcours
    y=y+np.sin(theta)*np.cos(phi)*libre_parcours
    z=z+np.cos(theta)*libre_parcours
    #calcul tableau des r²
    r2=np.square(x)+np.square(y)+np.square(z)
    r2moyen[i]=np.sum(r2)/nbe_particules
    dates[i]=i*tau

plt.figure(3)
plt.plot(dates,r2moyen,label='Simulation')
plt.plot(dates,dates*libre_parcours**2/tau,label='Théorie')
plt.grid()
plt.legend()
plt.xlabel('t')
plt.ylabel('<r²>')
plt.title('Marche au hasard à trois dimensions: <r²>=f(t)')







plt.show()





