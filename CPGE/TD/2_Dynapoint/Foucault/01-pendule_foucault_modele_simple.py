# -*- coding: utf-8 -*-
"""
Created on Wen Dec 31 16:12:01 2021

@author: JM Biansan
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from pour_animation import*


g=9.81
#################################################################################
#paramètres modifiables
#################################################################################
L=3 #longueur fil de suspension
jour_sideral=100 #valeur exagérée afin de rendre le phénomène visible sur une durée raisonnable
latitude_degre=45
nbe_periodes=20 #nombre de périodes sur lesquelles on fait le tracé
nbe_dates=2000 #le nbe de points de tracé
#conditions initiales
x0=0.5
ypoint0=0
#################################################################################
#fin des paramètres modifiables
#################################################################################

omega_terre=2*np.pi/jour_sideral
latitude=latitude_degre/180*np.pi
alpha=omega_terre*np.sin(latitude)
omega0=np.sqrt(g/L)
omega=np.sqrt(alpha**2+omega0**2)
T=2*np.pi/omega
#tracé sur nbe_periodes périodes
date_max=nbe_periodes*T
#les dates de tracé
Dates=np.linspace(0,date_max,nbe_dates)



#calcul des x et y: solution de d²X/dt²+2i.alpha.dX/dt+wo²X=0
x=x0*np.cos(alpha*Dates)*np.cos(omega*Dates)+(ypoint0+alpha*x0)/omega*np.sin(alpha*Dates)*np.sin(omega*Dates)
y=-x0*np.sin(alpha*Dates)*np.cos(omega*Dates)+(ypoint0+alpha*x0)/omega*np.cos(alpha*Dates)*np.sin(omega*Dates)

#initialisation des graphes
fig1 = plt.figure(1)
ax1 = plt.axes(xlim=(-x0, x0), ylim=(-x0,x0))
ax1.grid()
ax1.set_aspect('equal')
ax1.set_xlabel('x(m)')
ax1.set_ylabel('y(m)')
fig1.suptitle('Pendule de Foucault, modèle simple; L='+str(L)+'m, x0='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m, Jour sidéral='+str(jour_sideral)+'s, latitude='+str(latitude_degre)+'°',y=0.03)
courbe1, = ax1.plot([], [],'b',label='Trajectoire (vue de dessus)')
courbe_axe_tournant, = ax1.plot([], [],'r',label='Axe tournant à la vitesse angulaire -$\Omega_t sin\\lambda$')
ax1.legend()
date_modele1 = 'date = %.1fs'
date_text1 = ax1.text(0.05, 0.10, '', transform=ax1.transAxes)
param_axe=np.linspace(-x0,x0,100)

#la fonction appelé par Animateur pour le tracé à chaque date
def animate1(i):
    t=Dates[i]
    #l'astuce est de ne tracer que les points correspondants à dates antérieures à la iéme
    courbe1.set_data(x[:i],y[:i])
    courbe_axe_tournant.set_data(param_axe*np.cos(-alpha*t),param_axe*np.sin(-alpha*t))
    date_text1.set_text(date_modele1 % (t))
    return courbe1,courbe_axe_tournant,date_text1,

ani1 =Animateur(fig1, animate1, nombredates=nbe_dates,datemini=0,datemaxi=date_max,interval=10)


plt.show()