""" BIBLIOTHEQUES """
import numpy as np
import random as r
import matplotlib.pyplot as plt
from figure import *

""" PARAMETRES """
l   = 1           # distance des sauts
tau = 1           # durée entre sauts
D   = l**2/2/tau  # coefficient de diffusion

""" SIMULATION """
def marche(Nstep):
    x = np.zeros(Nstep)                               # position initiale
    for i in range(1,Nstep):               # boucle sur les sauts
        x[i] = x[i-1] + l*2*(r.randint(0,1)-1/2) # saut gauche ou droite
    return x                          # position finale au carre

N          = 1000
temps      = np.linspace(0, N*tau, N)
x1 = marche(N)
x2 = marche(N)
x3 = marche(N)

""" SIMULATION """
def marche_rapide(Nstep):
    x = 0                               # position initiale
    for i in range(1, Nstep):               # boucle sur les sauts
        x = x + l*2*(r.randint(0,1)-1/2) # saut gauche ou droite
    return x                          # position finale au carre

""" DISTANCE MOYENNE QUADRATIQUE """
def dquad(Nstep):
    xcarre = []                         # initialisation tableau
    for i in range(1000):               # 1000 simulations
        xcarre.append(marche_rapide(Nstep)**2)    # simulation d’une marche
    return np.mean(xcarre)     # moyenne quadratique

""" GRAPHIQUE """
# delta_theo = [2*D*t*tau for t in temps]
# delta_simu = [dquad(t) for t in temps]


# TRACÉ 

# Dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize(12)

# Creation de la figure
newfig()
ax = plt.gca()

# Parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

""" FIN NE PAS TOUCHER """

# Axe des abscisses 
nmbx = 6            # Nombre total de traits (i.e. nombres d'intervalles + 1)
xmin = 0            # Valeur minimale de x
xmax = N           # Valeur maximale de x

""" NE PAS TOUCHER """

plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [str('{}%.0f'%(i)).replace('.',',') for i in n.linspace(xmin,xmax,nmbx)]) # Ici vous pouver changer le nombre de decimales (.0f)
plt.xlim([xmin, xmax])

""" 
REMARQUE:
Pour le nombre de decimales, il est conseille d'en mettre le minimum possible afin d'alleger le graphe. 
.0f correspond a des entiers, .1f a un flottant avec un chiffre apres la virgule, etc.

"""

""" FIN NE PAS TOUCHER """

# Nom de la variable en abscisse
plt.xlabel(r'$t~(\tau)$')

# Petits traits intermediaires. NE PAS METTRE 0 DANS AutoMinorLocator, mais commenter la ligne pour les enlever.
minorLocator = AutoMinorLocator(2)          # Nombre de sous-intervalles dilimites par les petits traits
ax.xaxis.set_minor_locator(minorLocator)    # A enlever si vous ne voulez pas de petits traits

# Axe des ordonnees
nmby = 5	
ymin = -40
ymax = 40

# Si vous voulez l'echelle log
#plt.yscale('log')

# Si vous avez besoin de mettre les axes origines
ax.axhline(y=0, color='k', linewidth = 0.2)
# ax.axvline(x=0, color='k', linewidth = 0.2)

""" NE PAS TOUCHER """

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[str('{}%.0f'%(i)).replace('.',',') for i in n.linspace(ymin,ymax,nmby)]) # Ici vous pouver changer le nombre de decimales (.0f)
plt.ylim([ymin, ymax])

""" FIN NE PAS TOUCHER """

# Nom de la variable en ordonnee
plt.ylabel(r'$x~(\ell)$')

# Petits traits intermediaires
# ax.yaxis.set_minor_locator(minorLocator)

# Je mets n importe quoi dans les ordonnees a titre d'exemple, bien entendu.
# ploterr(size, mark, couleur,
#         temps, 
#         x1,
#         temps*0,
#         temps*0,
#         ID   = 0
#         )

# Modelisation. Attention plotcurve n'est pas la meme fonction que plt.plot !
plotcurve(size, mark, couleur,
	      temps,              	  # Abscisse
          x1,  	  # Ordonnee
          ID   = 0
          )
             
# Modelisation. Attention plotcurve n'est pas la meme fonction que plt.plot !
plotcurve(size, mark, couleur,
	      temps,              	  # Abscisse
          x2,  	  # Ordonnee
          ID   = 1
          )

plotcurve(size, mark, couleur,
	      temps,              	  # Abscisse
          x3,  	  # Ordonnee
          ID   = 2
          )
         
# Legende
leg(sub,                # NE PAS TOUCHER
    'upper left')       # Position de la legende sur le qraphe

# Save the figure
# figsave('marche1D_traj.pdf')   # Changer le nom de la figure

# """ GRAPHIQUE 2 """
# ploterr(size, mark, couleur,
#         temps, 
#         delta_simu,
#         temps*0,
#         temps*0,
#         ID   = 0
#         )
             
# # Modelisation. Attention plotcurve n'est pas la meme fonction que plt.plot !
# plotcurve(size, mark, couleur,
# 	      temps,              	  # Abscisse
#           delta_theo,  	  # Ordonnee
#           ID   = 1
#           )

# # plt.xlabel('t')                     # temps
# # plt.ylabel('delta')                 # delta
# plt.plot(temps,delta_simu,'b+')     # delta issu de la simulation
# plt.plot(temps,delta_theo,'r-')     # delta issu de la loi sqrt(D*t)
# plt.savefig('marche1D_x2.pdf')
# plt.show()
