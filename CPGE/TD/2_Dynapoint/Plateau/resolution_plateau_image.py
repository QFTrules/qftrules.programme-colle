import numpy as np
import matplotlib.pyplot as plt

""" PARAMÈTRES PHYSIQUES """
Omega = 2*np.pi/10 # vecteur rotation terrestre
v0    = 2         # vitesse initiale
R     = 1          # rayon du plateau

""" PARAMÈTRES PROGRAMME """
N    = 1000                     # nombre de points de tracé
tmax = 1.5*R/v0		                # temps maximal de tracé
t    = np.linspace(0,tmax,N)    # tableau des dates de tracé

""" TRACÉ """
# x = v0/np.sqrt(2)/Omega*np.cos(Omega*t)*np.sin(np.sqrt(2)*Omega*t)
# y = v0/np.sqrt(2)/Omega*np.sin(Omega*t)*np.sin(np.sqrt(2)*Omega*t)
x = v0*t*Omega*np.cos(Omega*t)
y = -v0*t*Omega*np.sin(Omega*t)

# plt.xlim(-1.5*d,1.5*d)
# plt.ylim(-1.5*d,1.5*d)

""" NE PAS TOUCHER """

#module de base pour les figures
from figure import *

#dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize()

#creation figure
newfig()
ax = plt.gca()

#parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

""" FIN NE PAS TOUCHER """

#axe des abscisses
nmbx = 5            #nombre de traits
xmin = -1*R            #valeur minimale de x
xmax = 1*R           #valeur maximale de x


plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [r'${}%.1f$'%(i) for i in n.linspace(xmin,xmax,nmbx)]) #changer .0f en le nombre de chiffres apres la virgule necessaire

#si jamais vous voulez modifier l'intervalle des axes a la main:
plt.xlim([xmin, xmax])

#nom de la variable en abscisse
plt.xlabel(r'$x$')

#petits traits intermediaires
minorLocator = AutoMinorLocator(1)          #changer le nombre de petits traits
ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 5
ymin = -1*R
ymax = 1*R

#si vous voulez l'echelle log:
#plt.yscale('log')

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[r'${}%.1f$'%(i) for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

#nom de la variable en ordonnee
plt.ylabel(r'$y$')

#petits traits intermediaires
minorLocator = AutoMinorLocator(1)
ax.yaxis.set_minor_locator(minorLocator)

circle = plt.Circle((0, 0), R, color='black', fill=False)
ax.add_patch(circle)

ax.set_aspect('equal')

plt.plot(x,y)
figsave('plateau_trajectoire_1')   #changer le nom de la figure
plt.show()
