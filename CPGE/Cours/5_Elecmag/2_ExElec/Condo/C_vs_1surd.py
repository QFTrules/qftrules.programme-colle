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
nmbx = 7            #nombre de traits
xmin = 0            #valeur minimale de x
xmax = 0.6           #valeur maximale de x


plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [(r'${}%.1f$'%(i)).replace('.',',\!') for i in n.linspace(xmin,xmax,nmbx)]) #changer .0f en le nombre de chiffres apres la virgule necessaire

#si jamais vous voulez modifier l'intervalle des axes a la main:
plt.xlim([xmin, xmax])

#nom de la variable en abscisse
unitx = 'mm'
plt.xlabel(r'$1/d$ (' + unitx + ')')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)          #changer le nombre de petits traits
ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 6
ymin = 0
ymax = 150

#si vous voulez l'echelle log:
#plt.yscale('log')

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[r'${}%.0f$'%(i) for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

#nom de la variable en ordonnee
unity = 'pF'
plt.ylabel(r'$C$ (' + unity + ')')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minorLocator)

#diametres
# Ta = 20

#donnees
data = n.loadtxt('aepinus.txt')
C   = n.array(data[1:,1])*1000
y = 1000/C
N = len(C)
d = n.array(data[1:,0])
x = 1/d
derr = n.array([0.01]*N)
xerr = derr/d**2
Cerr = n.array([1]*N)
yerr = Cerr/C**2

#regression lineaire: fit_affine ou fit_linear
(a0, a_err, b0, b_err, chi2) = fit_affine(x,     #abscisse
                                          C,     #ordonnee
                                          xerr, #incertitude abscisse
                                          Cerr) #incertitude ordonnee

# delta = -1/a0
# delta_err = a_err/a0**2
# T0mTa = n.exp(b0)

#print the results of the fit
print('    pente  = ' + '(%.2f +- %.2f)'%(a0,a_err) + unity + '/' + unitx + '\n')
print('    ordonnee  = ' + '(%.2f +- %.2f)'%(b0,b_err) + unity + '\n')
print('    chi2red  = ' + '%.2f  \n'%(chi2))

ploterr(size, mark, couleur,    #NE PAS TOUCHER
        x,                 #abscisse
        C,                 #ordonnee
        xerr,                  #incertitude abscisse
        Cerr,                  #incertitude ordonnee
        ID   = 0               #numero du type de points
        )

#modelisation
plt.plot(np.linspace(0,xmax,2),
         # T0mTa*n.exp(-x/delta) + Ta,
         b0 + a0*np.linspace(0,xmax,2),
         color      = couleur[0],   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
         )

#legende
leg(sub,                #NE PAS TOUCHER
    'lower right')       #position de la legende sur le qraphe

#save the figure
figsave('C_vs_unsurd')   #changer le nom de la figure
plt.show()


# PENSER À ATTENDRE L'ÉQUILIBRE THERMIQUE DE L'EAU QUI CIRCULE !
