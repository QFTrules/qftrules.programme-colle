"""             REGRESSION AFFINE               """
""" NE PAS TOUCHER """

#module de base pour les figures
from figure import *

#dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize(15)

#creation figure
newfig()
ax = plt.gca()

#parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

""" FIN NE PAS TOUCHER """

#axe des abscisses
nmbx = 6           #nombre de traits
xmin = 0            #valeur minimale de x
xmax = 10           #valeur maximale de x


plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [r'${}%.0f$'%(i) for i in n.linspace(xmin,xmax,nmbx)]) #changer .0f en le nombre de chiffres apres la virgule necessaire

#si jamais vous voulez modifier l'intervalle des axes a la main:
plt.xlim([xmin, xmax])

#nom de la variable en abscisse
plt.xlabel(r'$x$')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)          #changer le nombre de petits traits
ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 5
ymin = -4
ymax = 4

#si vous voulez l'echelle log:
#plt.yscale('log')

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[r'${}%.0f$'%(i) for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

#nom de la variable en ordonnee
plt.ylabel(r'$y$')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minorLocator)
ax.axhline(color=couleur[1])

import scipy.optimize as opt

# points expérimentaux
X = n.array([0, 2, 4, 6, 8, 10])            # absisse
Y = n.array([0.5, 7.9, 11, 17.5, 26, 31.8]) # ordonnée 3x+1 avec un bruit
DX = np.array([0.2, 0.1, 0.2, 0.2, 0.2, 0.2])   # incertitude absisse
DY = np.array([2, 2,0, 2, 2, 0])               # incertitude ordonnée
N = len(X)                                   # nombre de points de mesure

# régression affine
def residu(a,x,y):                           # résidu
    return y-a[0]*x-a[1]
# régression affine
def residu_incertitude(a,x,y,dx,dy):         # résidu avec incertitude
    return (y-a[0]*x-a[1])/np.sqrt(dy**2+a[0]**2*dx**2)
p = opt.leastsq(residu_incertitude,                      # moindre carré
                    [1,0],                   # estimation initiale de a et b
                    args = (X,Y,DX,DY),      # points expérimentaux
                    full_output = True)      # pour retourner les incertitudes

# paramètres optimaux
a, b             = p[0]                               # pente a et ordonnée à l’origine b
Delta_a, Delta_b = n.sqrt(n.abs(n.diagonal(p[1]))) # incertitudes-types sur a et b
khi2red          = sum(residu_incertitude([a,b],X,Y,DX,DY)**2)/(N-2)    # valeur du khi2 reduit

print(khi2red)

print(a,Delta_a)

ploterr(size, mark, couleur,    #NE PAS TOUCHER
        X,                 #abscisse
        residu([a,b],X,Y),                 #ordonnee
        0.2,                  #incertitude abscisse
        2,                  #incertitude ordonnee
        ID   = 0,               #numero du type de points
        name = r'' #nom de la courbe, le r permet d'ecrire en latex
        )

#modelisation
# plt.plot([xmin, xmax],
#          n.array([xmin, xmax])*a+b,
#          color      = couleur[0],   #couleur de la courbe, mettre le numero voulu
# #         label      = r'$\chi^2=%.2f$ '%(chi2)
#          )

#legende
leg(sub,                #NE PAS TOUCHER
    'lower right')       #position de la legende sur le qraphe

#save the figure
#figsave('Res')   #changer le nom de la figure