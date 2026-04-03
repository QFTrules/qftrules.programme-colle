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
nmbx = 9            #nombre de traits
xmin = 0            #valeur minimale de x
xmax = 1200         #valeur maximale de x


plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [r'${}%.0f$'%(i) for i in n.linspace(xmin,xmax,nmbx)]) #changer .0f en le nombre de chiffres apres la virgule necessaire

#si jamais vous voulez modifier l'intervalle des axes a la main:
plt.xlim([xmin, xmax])

#nom de la variable en abscisse
plt.xlabel(r'$\Phi$ (lux)')

#petits traits intermediaires
minorLocator = AutoMinorLocator(1)          #changer le nombre de petits traits
ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 7
ymin = 0
ymax = 100

#si vous voulez l'echelle log:
#plt.yscale('log')

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[r'${}%.0f$'%(i) for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

#nom de la variable en ordonnee
plt.ylabel(r'$I_{\rm ph}$ (µA)')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minorLocator)

#load the first set of data
dictio = {0:'moyen', 1:'gros', 2:'alu'}

#diametres
Ta = 20

""" ALU """
data = n.loadtxt('sensibilite.txt')
T   = data[:,1]
print(x)
x = data[:,0]
N = len(T)
T0  = T[0]
# Tlog = n.log(T-Ta)
# pix = 18.9/66 # mm
# x   = n.linspace(0,N*pix,N)
xerr = x*0.05
Terr = T*0.05
# Terrlog = Terr/(T-Ta)

#regression lineaire: fit_affine ou fit_linear
(a0, a_err, b0, b_err, chi2) = fit_affine(x,     #abscisse
                                          T,     #ordonnee
                                          xerr, #incertitude abscisse
                                          Terr) #incertitude ordonnee

# delta = -1/a0
# delta_err = a_err/a0**2
# T0mTa = n.exp(b0)

#print the results of the fit
print('    pente  = ' + '(%.2f +- %.2f)K.mm^-1  \n'%(a0,a_err))
print('    T0  = ' + '(%.2f +- %.2f)°C  \n'%(b0,b_err))
print('    chi2red  = ' + '%.2f  \n'%(chi2))

ploterr(size, mark, couleur,    #NE PAS TOUCHER
        x,                 #abscisse
        T,                 #ordonnee
        xerr,                  #incertitude abscisse
        Terr,                  #incertitude ordonnee
        ID   = 0               #numero du type de points
        )

#modelisation
plt.plot(x,
         # T0mTa*n.exp(-x/delta) + Ta,
         b0 + a0*x,
         color      = couleur[0],   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
         )
#
# """ CUIVRE """
# data = n.loadtxt('Profil_T_laiton3.txt')
# T   = data[:,1]
# N = len(T)
# T0  = T[0]
# Tlog = n.log(T-Ta)
# x   = n.linspace(0,N*0.5,N)
# xerr = n.array([0.1]*N)
# Terr = n.array([1]*N)
# Terrlog = Terr/(T-Ta)
#
#
#
# #regression lineaire: fit_affine ou fit_linear
# (a0, a_err, b0, b_err, chi2) = fit_affine(x,     #abscisse
# Tlog,     #ordonnee
# xerr, #incertitude abscisse
# Terrlog) #incertitude ordonnee
#
# delta = -1/a0
# T0mTa = n.exp(b0)
#
# #print the results of the fit
# print('    delta_cuivre  = ' + '%.2f cm \n'%(delta))
#
# ploterr(size, mark, couleur,    #NE PAS TOUCHER
# x[::5],                 #abscisse
# T[::5],                 #ordonnee
# xerr[::5],                  #incertitude abscisse
# Terr[::5],                  #incertitude ordonnee
# ID   = 1               #numero du type de points
# )
#
# #modelisation
# plt.plot(x,
# T0mTa*n.exp(-x/delta) + Ta,
# color      = couleur[1],   #couleur de la courbe, mettre le numero voulu
# #         label      = r'$\chi^2=%.2f$ '%(chi2)
# )

#legende
leg(sub,                #NE PAS TOUCHER
    'lower right')       #position de la legende sur le qraphe

#save the figure
figsave('sensibilite')   #changer le nom de la figure
plt.show()


# PENSER À ATTENDRE L'ÉQUILIBRE THERMIQUE DE L'EAU QUI CIRCULE !
