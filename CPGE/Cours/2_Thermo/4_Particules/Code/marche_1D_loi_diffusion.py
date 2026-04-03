""" BIBLIOTHEQUES """
import numpy as np
import random as r
import matplotlib.pyplot as plt
from figure import *

""" PARAMETRES """
l   = 1           # distance des sauts
tau = 1           # durée entre sauts
D   = l**2/2/tau  # coefficient de diffusion

# """ SIMULATION """
# def marche(Nstep):
#     x = np.zeros(Nstep)                               # position initiale
#     for i in range(1,Nstep):               # boucle sur les sauts
#         x[i] = x[i-1] + l*2*(r.randint(0,1)-1/2) # saut gauche ou droite
#     return x                          # position finale au carre

N          = 100
temps      = np.linspace(0, N*tau, N)
# x1 = marche(N)
# x2 = marche(N)
# x3 = marche(N)

""" SIMULATION """
def marche_rapide(Nstep):
    x = 0 
    i = 0                           # position initiale
    # print(i,Nstep)
    while i < Nstep:               # boucle sur les sauts
        x = x + l*2*(r.randint(0,1)-1/2) # saut gauche ou droite
        i += 1
    return x                          # position finale au carre

""" DISTANCE MOYENNE QUADRATIQUE """
def dquad(Nstep):
    xcarre = []                         # initialisation tableau
    for i in range(1000):               # 1000 simulations
        xcarre.append(marche_rapide(Nstep)**2)    # simulation d’une marche
    return np.mean(xcarre)     # moyenne quadratique

""" GRAPHIQUE """
quad_theo = 2*D*temps*tau
delta_theo = np.sqrt(quad_theo)
quad_simu = [dquad(t) for t in temps]
delta_simu = np.sqrt(quad_simu)


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
plt.xlabel(r'$t$')

# Petits traits intermediaires. NE PAS METTRE 0 DANS AutoMinorLocator, mais commenter la ligne pour les enlever.
minorLocator = AutoMinorLocator(2)          # Nombre de sous-intervalles dilimites par les petits traits
ax.xaxis.set_minor_locator(minorLocator)    # A enlever si vous ne voulez pas de petits traits

# Axe des ordonnees
nmby = 6	
ymin = 0
ymax = 10

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
plt.ylabel(r'$\delta(t)$')

# Petits traits intermediaires
minorLocator = AutoMinorLocator(2)          # Nombre de sous-intervalles dilimites par les petits traits
ax.yaxis.set_minor_locator(minorLocator)

# Je mets n importe quoi dans les ordonnees a titre d'exemple, bien entendu.
ploterr(size, mark, couleur,
        temps[::2], 
        delta_simu[::2],
        temps[::2]*0,
        temps[::2]*0,
        ID   = 0,
        name=r'Simulation 1D'
        )

# # Modelisation. Attention plotcurve n'est pas la meme fonction que plt.plot !
# plotcurve(size, mark, couleur,
# 	      temps,              	  # Abscisse
#           delta_simu,  	  # Ordonnee
#           ID   = 0
#           )
             
# Modelisation. Attention plotcurve n'est pas la meme fonction que plt.plot !
plotcurve(size, mark, couleur,
	      temps,              	  # Abscisse
          delta_theo,  	  # Ordonnee
          ID   = 1,
          name=r'$\delta = \sqrt{2D t}$'
          )


""" INSET """

# # Creation de l'insert
# ax_inset = inset_axes(sub,                      # NE PAS TOUCHER
#                       width          = "35%",   # Largeur relative
#                       height         = "35%",   # Hauteur relative
#                       loc            = 4,       # Code pour la position
#                       borderpad      = 2)       # Distance au cadre exterieur

# #a% Axe des abscisses
# nmbx = 6
# xmin = 0
# xmax = 100

# # Memes remarques qu'au debut pour changer les axes
# ax_inset.set_xticks(n.linspace(xmin, xmax, nmbx))
# ax_inset.set_xticklabels([str('{}%.0f'%(i)).replace('.',',') for i in n.linspace(ymin,ymax,nmby)])
# ax_inset.set_xlim([xmin, xmax])

# # Axe des ordonnes
# nmby = 6
# ymin = 0
# ymax = 10

# ax_inset.set_yticks(n.linspace(ymin, ymax, nmby))
# ax_inset.set_yticklabels([str('{}%.0f'%(i)).replace('.',',') for i in n.linspace(ymin,ymax,nmby)])
# ax_inset.set_ylim([ymin, ymax])

# # Plot
# inset_ploterr(ax_inset, size, mark, couleur,    #NE PAS TOUCHER
#         temps,                                      #abscisse
#         quad_simu,                                 #ordonnee
#         temps*0,                                  #incertitude abscisse
#         temps*0,                                  #incertitude ordonne
#         ID   = 0                                #numero du type de points
# )
         
# Legende
leg(sub,                # NE PAS TOUCHER
    'lower right')       # Position de la legende sur le qraphe

# Save the figure
figsave('marche1D_loi_diffusion.pdf')   # Changer le nom de la figure

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
