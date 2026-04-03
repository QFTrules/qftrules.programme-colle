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
latitude_degre=45
jour_sideral=86164
nbe_periodes=50 #nombre de périodes sur lesquelles on fait le tracé
nbe_dates=5000 #le nbe de points de tracé
#conditions initiales
x0=0.5
ypoint0=0.01

#################################################################################
#fin des paramètres modifiables
#################################################################################



latitude=latitude_degre/180*np.pi
CL=np.cos(latitude)
SL=np.sin(latitude)
omega_terre=2*np.pi/jour_sideral
alpha=omega_terre*np.sin(latitude)
L2=np.power(L,2)
omega0=np.sqrt(g/L)
T0=2*np.pi/omega0
date_max=nbe_periodes*T0
omega_Puiseux=3/8*omega0/L2*x0*ypoint0/omega0


#le ypoint0 qui fait que ça ne précesse pas: omega_Puiseux=omega_Terre.sin latitude
#print(8/3*omega_terre*SL*L2/x0)

#le ypoint0 qui fait que la vitesse angulaire de diffère pas de plus de 1% de celle prévue par Coriolis pur
# |omega+alpha|<|alpha|/100, soit |ypoint0|<8/3.|alpha|/(100.x0)
#print(8/3*omega_terre*SL*L2/100/x0)
#et le 1/2 petit axe correspondant
#print(8/3*omega_terre*SL*L2/100/x0/omega0)

y0=0
xpoint0=0
conditions_initiales=[x0,y0,xpoint0,ypoint0]



def equations(X,t):
    #X est (x,y,dx/dt,dy/dt)
    #equations renvoie dX/dt
    x=X[0]
    y=X[1]
    xpoint=X[2]
    ypoint=X[3]
    r2=np.power(x,2)+np.power(y,2)
    xpp=-g/L*x*np.sqrt(1-r2/L2)-x/L2*(np.power(xpoint,2)+np.power(ypoint,2))-x/L2*np.power(x*xpoint+y*ypoint,2)/(L2-r2)
    xpp=xpp-2*omega_terre*CL/L2/np.sqrt(L2-r2)*(x*xpoint*np.power(y,2)+np.power(y,3)*ypoint+y*ypoint*(L2-r2))
    xpp=xpp+2*omega_terre*SL/L2*(np.power(y,2)*ypoint+x*xpoint*y+ypoint*(L2-r2))
    ypp=-g/L*y*np.sqrt(1-r2/L2)-y/L2*(np.power(xpoint,2)+np.power(ypoint,2))-y/L2*np.power(x*xpoint+y*ypoint,2)/(L2-r2)
    ypp=ypp+2*omega_terre*CL/L2/np.sqrt(L2-r2)*(np.power(x,2)*xpoint*y+x*np.power(y,2)*ypoint+xpoint*y*(L2-r2))
    ypp=ypp-2*omega_terre*SL/L2*(np.power(x,2)*xpoint+x*y*ypoint+xpoint*(L2-r2))
    return([xpoint,ypoint,xpp,ypp])

dates=np.linspace(0,date_max,nbe_dates)
#résolution par odeint
res=odeint(equations,conditions_initiales,dates)
#on récupère x et y
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
angle_polaire_max=0
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
            if (np.abs(np.arctan2(y[i],x[i]))>angle_polaire_max) and (np.abs(np.arctan2(y[i],x[i]))<np.pi/2):
                angle_polaire_max=np.abs(np.arctan2(y[i],x[i]))
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
ax1 = plt.axes(xlim=(-x0, x0), ylim=(-x0*np.sin(angle_polaire_max)*1.2,x0*np.sin(angle_polaire_max)*1.2))
ax1.grid()
#ax1.set_aspect('equal')
ax1.set_xlabel('x(m)')
ax1.set_ylabel('y(m)')
fig1.suptitle('Pendule de Foucault, modèle sans frottements; L='+str(L)+'m, x0='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m', y=0.03)
courbe_axe_tournant, = ax1.plot([], [],'r',label='Axe tournant à la vitesse angulaire $\Omega_{Puiseux}$-$\Omega_t sin\\lambda$')
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
    courbe_axe_tournant.set_data(param_axe*np.cos((omega_Puiseux-alpha)*t),param_axe*np.sin((omega_Puiseux-alpha)*t))
    date_text1.set_text(date_modele1 % (t))
    return courbe_axe_tournant,courbe1,date_text1,

ani1 =Animateur(fig1, animate1, nombredates=nbe_dates,datemini=0,datemaxi=date_max,interval=10)

fig0,(ax01) = plt.subplots(1,1)
ax01.plot(x,y)
ax01.grid()
ax01.set_xlabel('x(m)')
ax01.set_ylabel('y(m)')
fig0.suptitle('Pendule de Foucault, modèle sans frottements, L='+str(L)+'m, x(0)='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s')


fig2,(ax21) = plt.subplots(1,1)
ax21.plot(dates_rmax,angle_polaire_rmax,label='numérique')
ax21.plot(dates_rmax,omega_Puiseux*np.array(dates_rmax),label='avec précession de Puiseux seule')
ax21.plot(dates_rmax,-alpha*np.array(dates_rmax),label='avec précession de Coriolis seule')
ax21.plot(dates_rmax,(omega_Puiseux-alpha)*np.array(dates_rmax),label='Puiseux + Coriolis')
ax21.set_xlabel('t(s)')
ax21.set_ylabel('angle polaire (rad)')
ax21.grid()
ax21.legend()
ax21.set_title('Angle polaire du grand axe en fonction du temps')
fig2.suptitle('Précession du pendule de Foucault, L='+str(L)+'m, x(0)='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s')




plt.show()