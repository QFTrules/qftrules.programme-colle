# -*- coding: utf-8 -*-
"""
Created on Wen Dec 31 16:12:01 2021

@author: JM Biansan
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

g=9.81

#################################################################################
#paramètres modifiables
#################################################################################
L=3 #longueur fil de suspension
nbe_periodes=50 #nombre de périodes sur lesquelles on fait le tracé
nbe_dates=5000 #le nbe de points de tracé
#conditions initiales
x0=0.5
ypoint0=0.5

#################################################################################
#fin des paramètres modifiables
#################################################################################

y0=0
xpoint0=0
conditions_initiales=[x0,y0,xpoint0,ypoint0]

L2=np.power(L,2)
omega0=np.sqrt(g/L)
T0=2*np.pi/omega0
date_max=nbe_periodes*T0


def equations(X,t):
    #X est (x,y,dx/dt,dy/dt)
    #equations renvoie dX/dt
    x=X[0]
    y=X[1]
    xpoint=X[2]
    ypoint=X[3]
    r2=np.power(x,2)+np.power(y,2)
    xpp=-omega0*x*np.sqrt(1-r2/L2)-x/L2*(np.power(xpoint,2)+np.power(ypoint,2))-x/L2*np.power(x*xpoint+y*ypoint,2)/(L2-r2)
    ypp=-omega0*y*np.sqrt(1-r2/L2)-y/L2*(np.power(xpoint,2)+np.power(ypoint,2))-y/L2*np.power(x*xpoint+y*ypoint,2)/(L2-r2)
    return(np.array([xpoint,ypoint,xpp,ypp]))

dates=np.linspace(0,date_max,nbe_dates)
#résolution par odeint
res=odeint(equations,conditions_initiales,dates)
#on récupère x et y, ainsi que dx/dt et dy/dt
x=res[:,0]
y=res[:,1]
#calcul de z en utilisant la longueur du pendule: x²+y²+(z-L)²=L²
z=L-np.sqrt(np.power(L,2)-np.power(x,2)-np.power(y,2))
xyz = np.array([x, y, z])



#animation de la précession
#initialisation des graphes
fig1 = plt.figure(1)
ax1=Axes3D(fig1)
ax1.grid()
#ax1.set_aspect('equal')
ax1.set_xlabel('x(m)')
ax1.set_ylabel('y(m)')
ax1.set_zlabel('z(m)')
fig1.suptitle('Pendule sphérique; L='+str(L)+'m, x0='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s (figure orientable à la souris)', y=0.03)
courbe1 = ax1.plot(xyz[0], xyz[1],xyz[2],'b')[0]

date_modele1 = 'date = %.1fs'
date_text1 = ax1.text(0.05, 0.10,0.05, '', transform=ax1.transAxes)


#la fonction appelé par Animateur pour le tracé à chaque date
def animate1(i):
    #pour accélérer le tracé, on ne trace que toutes les 10 dates
    if i%10 !=0:
        return
    t=dates[i]
    #l'astuce est de ne tracer que les points correspondants à dates antérieures à la iéme
    courbe1.set_data(xyz[0:2,:i])
    courbe1.set_3d_properties(xyz[2, :i])
    date_text1.set_text(date_modele1 % (t))
    return courbe1,date_text1

ani1 =FuncAnimation(fig1, animate1, frames=nbe_dates,interval=10)


#tracé de la trajectoire sans animation
fig0 = plt.figure()
ax01 = fig0.add_subplot(projection='3d')
ax01.plot(x,y,z)
ax01.set_xlabel('x(m)')
ax01.set_ylabel('y(m)')
ax01.set_zlabel('z(m)')

ax01.grid()

fig0.suptitle('Précession du pendule sphérique, L='+str(L)+'m, x(0)='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s (figure orientable à la souris)')







plt.show()