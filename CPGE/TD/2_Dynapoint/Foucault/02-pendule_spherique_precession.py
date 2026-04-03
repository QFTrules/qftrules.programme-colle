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
xpoint=res[:,2]
ypoint=res[:,3]

################################################
#recherche des valeurs successives de l'ange polaire du grand axe
################################################
#on calcule r²=x²+y²
r2=np.power(x,2)+np.power(y,2)
#on cherche les dates où r est max
dates_rmax=[0] #on suppose que le point de départ correspond à un max
dates_rmin=[]
angle_polaire_rmax=[0]
demi_grand_axe=[np.sqrt(r2[0])]
demi_petit_axe=[]

i=2
#max_pair et min_pair évitent de compter 2 fois les min et les max sur chaque période
max_pair=False
min_pair=True
while i<nbe_dates-1:
    if r2[i-1]<r2[i] and r2[i+1]<r2[i]:
        #on a trouvé un max
        if max_pair:
            dates_rmax.append(dates[i])
            angle_polaire_rmax.append(np.arctan2(y[i],x[i]))
            demi_grand_axe.append(np.sqrt(r2[i]))
        max_pair=not(max_pair)
    elif r2[i-1]>r2[i] and r2[i+1]>r2[i]:
        #on a trouvé un min
        if min_pair:
            dates_rmin.append(dates[i])
            demi_petit_axe.append(np.sqrt(r2[i]))
        min_pair=not(min_pair)
    i=i+1

################################################
#fin recherche des valeurs successives de l'ange polaire du grand axe
################################################






#animation de la précession
#initialisation des graphes
fig1 = plt.figure(1)
ax1 = plt.axes(xlim=(-x0, x0), ylim=(-x0,x0))
ax1.grid()
ax1.set_aspect('equal')
ax1.set_xlabel('x(m)')
ax1.set_ylabel('y(m)')
fig1.suptitle('Pendule sphérique; L='+str(L)+'m, x0='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m', y=0.03)
courbe_axe_tournant, = ax1.plot([], [],'r',label='Axe tournant à la vitesse angulaire $\Omega_{Puiseux}$')
courbe1, = ax1.plot([], [],'b',label='Trajectoire (vue de dessus)')
ax1.legend()
date_modele1 = 'date = %.1fs'
date_text1 = ax1.text(0.05, 0.10, '', transform=ax1.transAxes)
param_axe=np.linspace(-x0,x0,100)

#la fonction appelé par Animateur pour le tracé à chaque date
def animate1(i):
    #pour accélérer le tracé, on ne trace que toutes les 10 dates
    if i%10 !=0:
        return
    t=dates[i]
    #l'astuce est de ne tracer que les points correspondants à dates antérieures à la iéme
    courbe1.set_data(x[:i],y[:i])
    courbe_axe_tournant.set_data(param_axe*np.cos(3/8*omega0/L2*x0*ypoint0/omega0*t),param_axe*np.sin(3/8*omega0/L2*x0*ypoint0/omega0*t))
    date_text1.set_text(date_modele1 % (t))
    return courbe_axe_tournant,courbe1,date_text1,

ani1 =Animateur(fig1, animate1, nombredates=nbe_dates,datemini=0,datemaxi=date_max,interval=10)


#tracé de la trajectoire sans animation
fig0,(ax01) = plt.subplots(1,1)
ax01.plot(x,y)
ax01.set_xlabel('x(m)')
ax01.set_ylabel('y(m)')
ax01.grid()

fig0.suptitle('Précession du pendule sphérique, L='+str(L)+'m, x(0)='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s')


#tracé de l'angle polaire ne fonction du temps, et superposition avec la formule de Puiseux
fig2,(ax21) = plt.subplots(1,1)
ax21.plot(dates_rmax,angle_polaire_rmax,label='numérique')
ax21.plot(dates_rmax,3/8*omega0/L2*x0*ypoint0/omega0*np.array(dates_rmax),label='avec formule de Puiseux')
ax21.set_xlabel('t(s)')
ax21.set_ylabel('angle polaire (rad)')
ax21.grid()
ax21.legend()
ax21.set_title('Angle polaire du grand axe en fonction du temps')
fig2.suptitle('Précession du pendule sphérique, L='+str(L)+'m, x(0)='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s')





plt.show()