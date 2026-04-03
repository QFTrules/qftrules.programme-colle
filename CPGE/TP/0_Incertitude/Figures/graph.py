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
nmbx = 6           #nombre de traits
xmin = 0            #valeur minimale de x
xmax = 5           #valeur maximale de x


plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [r'${}%.0f$'%(i) for i in n.linspace(xmin,xmax,nmbx)]) #changer .0f en le nombre de chiffres apres la virgule necessaire

#si jamais vous voulez modifier l'intervalle des axes a la main:
plt.xlim([xmin, xmax])

#nom de la variable en abscisse
plt.xlabel(r'$t$ (s)')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)          #changer le nombre de petits traits
ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 6
ymin = 0
ymax = 5

#si vous voulez l'echelle log:
#plt.yscale('log')

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[r'${}%.1f$'%(i) for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

#nom de la variable en ordonnee
plt.ylabel(r'$z$ (cm)')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minorLocator)

#load the first set of data
dictio = {0:'moyen', 1:'gros', 2:'alu'}

#diametres
d_2 = 1.42*10**(-2)
d_1 = 1.20*10**(-2)
d_3 = 1.40*10**(-2)
dico = {0:d_1, 1:d_2, 2:d_3}
N    = {0:7, 1:7, 2:6}

#number of fluxmeters in the exp.
data = n.loadtxt('R2_vs_m.txt')
x    = data[:,0]
y    = (3.343-n.array(data[:,1]))**2

#incertitudes
y_err   = 0.05*2*n.array(data[:,1])
x_err   = n.zeros(len(x))

#regression lineaire: fit_affine ou fit_linear
(a0, a_err, b0, b_err, chi2) = fit_affine(x,     #abscisse
                                          y,     #ordonnee
                                          x_err, #incertitude abscisse
                                          y_err) #incertitude ordonnee

#print the results of the fit
print('       a      = %.3e +/- %.1e\n'%(a0, a_err)
      + '       b      = %.3e +/- %.1e\n'%(b0, b_err)
      + '       chi2     = %.3f \n'%(chi2) )

ploterr(size, mark, couleur,    #NE PAS TOUCHER
        x,                 #abscisse
        y,                 #ordonnee
        x_err,                  #incertitude abscisse
        y_err,                  #incertitude ordonnee
        ID   = 0,               #numero du type de points
        name = r'' #nom de la courbe, le r permet d'ecrire en latex
        )

#modelisation
plt.plot([xmin, xmax],
         n.array([xmin, xmax])*a0+b0,
         color      = couleur[0],   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
         )

#legende
leg(sub,                #NE PAS TOUCHER
    'lower right')       #position de la legende sur le qraphe

#save the figure
figsave('R2_vs_m')   #changer le nom de la figure
