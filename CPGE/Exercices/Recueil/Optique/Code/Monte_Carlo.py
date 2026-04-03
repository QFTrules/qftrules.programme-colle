# Fonction donnant f’
def focale(objet,image):
    return 1/(1/image - 1/objet)

# Importation des bibliothèques
# import numpy as np
# import matplotlib.pyplot as plt
from figure import *

# Dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize()

# Creation de la figure
newfig()
ax = plt.gca()

# Parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

""" FIN NE PAS TOUCHER """

minorLocator = AutoMinorLocator(3)          # Nombre de sous-intervalles dilimites par les petits traits
ax.xaxis.set_minor_locator(minorLocator) 

# Axe des abscisses 
nmbx = 9           # Nombre total de traits (i.e. nombres d'intervalles + 1)
xmin = 9            # Valeur minimale de x
xmax = 11           # Valeur maximale de x


""" NE PAS TOUCHER """

plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [str('{}%.1f'%(i)).replace('.',',') for i in n.linspace(xmin,xmax,nmbx)]) # Ici vous pouver changer le nombre de decimales (.0f)
plt.xlim([xmin, xmax])

""" 
REMARQUE:
Pour le nombre de decimales, il est conseille d'en mettre le minimum possible afin d'alleger le graphe. 
.0f correspond a des entiers, .1f a un flottant avec un chiffre apres la virgule, etc.

"""

""" FIN NE PAS TOUCHER """

minorLocator = AutoMinorLocator(2)          # Nombre de sous-intervalles dilimites par les petits traits
ax.yaxis.set_minor_locator(minorLocator) 

# Nom de la variable en abscisse
plt.xlabel(r'$t$ (min)')

# Axe des ordonnees
nmby = 5
ymin = 0
ymax = 400

# Si vous voulez l'echelle log
#plt.yscale('log')

# Si vous avez besoin de mettre les axes origines
#ax.axhline(y=0, color='k', linewidth = 0.2)
#ax.axvline(x=0, color='k', linewidth = 0.2)

""" NE PAS TOUCHER """

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[str('{}%.0f'%(i)).replace('.',',') for i in n.linspace(ymin,ymax,nmby)]) # Ici vous pouver changer le nombre de decimales (.0f)
plt.ylim([ymin, ymax])

""" FIN NE PAS TOUCHER """

# Nom de la variable en ordonnee
#plt.ylabel(r'Nombre')






# Positions de l'objet et de l'image
OA  = -15   # cm
OAp = 30    # cm

# Incertitude-type
Delta = 1   # cm

N  = 10   # nombre de tirages
fp = []      # liste des valeurs de f'

for i in range(N):
    objet = n.random.uniform(OA-Delta,OA+Delta)    # tirage de OA
    image = n.random.uniform(OAp-Delta,OAp+Delta)  # tirage de OAp
    fp.append(focale(objet,image))                  # calcul de f'

plt.hist(fp,
         bins = 40)  # histogramme
plt.title(r"Distribution de f'")
plt.xlabel(r"f' (cm)")
#plt.show()

# Save the figure
#figsave('distrib_f')   # Changer le nom de la figure
#plt.show()

fmoy    = np.mean(fp)       # valeur moyenne de f'
Deltaf  = np.std(fp,ddof=1) # �cart-type de la distribution de f'
print("f' = (%.3f \pm %.3f) cm"%(fmoy,Deltaf))
