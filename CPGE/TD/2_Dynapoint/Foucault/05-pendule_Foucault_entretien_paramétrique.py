# -*- coding: utf-8 -*-
"""
Created on Wen Dec 31 16:12:01 2021

@author: JM Biansan
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt



g=9.81

#################################################################################
#paramètres modifiables
#################################################################################
L=67 #longueur fil de suspension du pendule du Panthéon
masse=28#masse du pendule du Panthéon
latitude_degre=48.856614#celle de Paris
jour_sideral=86164
nbe_periodes=2000 #nombre de périodes sur lesquelles on fait le tracé: correspond à 6h
nbe_dates=100000 #le nbe de points de tracé
#conditions initiales
x0=3
ypoint0=0
rho_air=1.2#masse volumique de l'air
rayon=0.38/2#rayon de la sphère
Cx=0.45#le coefficient de traînée: 0.45 pour une sphère lisse
eta_air=18.5e-6#coefficient de viscosite de l'air
d=4/3/np.pi/masse*L**2*x0/L*0.5*rho_air*np.pi*rayon**2*Cx

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
omega02=g/L
T0=2*np.pi/omega0
omega=np.sqrt(alpha**2+omega0**2)
omega2=alpha**2+omega0**2
T=2*np.pi/omega
date_max=nbe_periodes*T0

coef_frottement=0.5*rho_air*np.pi*rayon**2*Cx


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
    v=np.sqrt(np.power(xpoint,2)+np.power(ypoint,2))
    r2=np.power(x,2)+np.power(y,2)
    xpp=-omega02*x+2*alpha*ypoint-coef_frottement*v*xpoint/masse-4*omega2*d/L*np.sin(2*omega*t)*x
    ypp=-omega02*y-2*alpha*xpoint-coef_frottement*v*ypoint/masse-4*omega2*d/L*np.sin(2*omega*t)*y
    return([xpoint,ypoint,xpp,ypp])

dates=np.linspace(0,date_max,nbe_dates)
#résolution par odeint
res=odeint(equations,conditions_initiales,dates)
#on récupère x et y
x=res[:,0]
y=res[:,1]
xpoint=res[:,2]
ypoint=res[:,3]
v=np.sqrt(np.power(xpoint,2)+np.power(ypoint,2))

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



#tracé de la trajectoire
fig0,(ax01) = plt.subplots(1,1)
ax01.plot(x,y)
ax01.grid()
ax01.set_xlabel('x(m)')
ax01.set_ylabel('y(m)')
fig0.suptitle('Précession du pendule de Foucault entrenu paramétriquement, L='+str(L)+'m, x(0)='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s')

#tracé du demi grand-axe en fonction du temp
fig2,(ax21) = plt.subplots(1,1)
ax21.set_ylim(0,x0*1.1)
ax21.plot(np.array(dates_rmax)/3600,demi_grand_axe)
ax21.set_xlabel('t(h)')
ax21.set_ylabel('Demi grand-axe (en m)')
ax21.grid()
ax21.set_title('Demi grand axe en fonction du temps')
fig2.suptitle('Pendule de Foucault entrenu paramétriquement, L='+str(L)+'m, x(0)='+str(x0)+'m, dy/dt(0)='+str(ypoint0)+'m/s')



plt.show()