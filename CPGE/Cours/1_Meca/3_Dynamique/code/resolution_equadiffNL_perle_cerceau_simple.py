"""
Solve a non linear differential equation in Python.
Autor : L. Villa
Modified by Eric Brillaux, 2022-2023
"""

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def model(system,t,omega_0,omega,h):
    theta = system[0]
    xi = system[1]
    theta_point = xi
    xi_point = -(omega_0**2)*np.sin(theta) + (omega**2)*np.sin(theta)*np.cos(theta)-h*xi
    system_point = [theta_point,xi_point]
    return system_point

omega_0=np.sqrt(9.81/1) #rayon cercle=1
omega=1.1*omega_0
h=0.5
system_0 = [np.pi/4,0] #condition initiale (theta,theta_point)
t=np.linspace(0,20,200)
system = odeint(model,system_0,t,args =(omega_0,omega,h))
plt.plot(t,system[:,0],label=r'$\theta$')
plt.plot(t,np.mean(system[:,0])*np.ones(len(t)),'--',label=r'$\theta_{\rm{eq}}$')

plt.xlabel(r'$t$')
plt.ylabel(r'$\theta$')
plt.ylim(-1,1)
plt.title(r'$\theta(0)\simeq$'+'{:0.3f}'.format(system_0[0])+','
        +r'$\dot{\theta}(0)=$'+str(system_0[1])+',
        +r'$\omega/\omega_0=$'+str(omega/omega_0))
plt.legend(loc='best')
plt.show()
print(np.mean(system[:,0]))


# animation du mouvement
frame=1
angle=np.linspace(0,2*np.pi,200) #pour paramétrer l'équation de l'anneau
for i in system[:,0]:
    x=np.sin(i) #avec un rayon de l'anneau de 1, la composante du mouvement selon e_{x'} est sin(theta)
    z=-np.cos(i) #avec un rayon de l'anneau de 1, la composante du mouvement selon e_{z'} est -cos(theta)
    filename=str(frame)+'.png'
    frame=frame+1
    plt.figure()
    plt.plot([0,0],[1.5,0],color='k') #axe e_{z}
    plt.plot([0,0],[-1.5,0],color='k') #axe e_{z}
    plt.plot([1.5,0],[0,0],color='k') #axe e_{x'}
    plt.plot([-1.5,0],[0,0],color='k') #axe e_{x'}
    plt.plot(np.cos(angle),np.sin(angle),color='blue') #anneau
    plt.plot(x,z,'o',markersize=10,color='red') #mouvement de la perle
    plt.xlim([-1.5,1.5])
    plt.ylim([-1.5,1.5])
    plt.title(r'$\theta(0)=\pi/4$,'
            +r'$\dot{\theta}(0)=$'+str(system_0[1])+',
            +r'$\omega/\omega_0=$'+str(omega/omega_0)+',
            +r'$h=$'+str(h))
    plt.savefig('motion/'+filename)
    plt.close()
