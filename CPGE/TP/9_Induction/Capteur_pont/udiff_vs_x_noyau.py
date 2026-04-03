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
nmbx = 11            #nombre de traits
xmin = 0            #valeur minimale de x
xmax = 200          #valeur maximale de x


plt.xticks([ i for i in n.linspace(xmin,xmax,nmbx)],
    [r'${}%.0f$'%(i) for i in n.linspace(xmin,xmax,nmbx)]) #changer .0f en le nombre de chiffres apres la virgule necessaire

#si jamais vous voulez modifier l'intervalle des axes a la main:
plt.xlim([xmin, xmax])

#nom de la variable en abscisse
unitx = 'mm'
plt.xlabel(r'$x$ (' + unitx + ')')

#petits traits intermediaires
minorLocator = AutoMinorLocator(1)          #changer le nombre de petits traits
ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 6
ymin = 0
ymax = 2.5

#si vous voulez l'echelle log:
#plt.yscale('log')

plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
	[r'${}%.1f$'%(i) for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

#nom de la variable en ordonnee
unity = 'V'
plt.ylabel(r'$U_{\rm eff}$ (' + unity + ')')

#petits traits intermediaires
minorLocator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minorLocator)

#diametres
# Ta = 20

""" ALU """
data = n.loadtxt('push_pull_noyau.txt')
x = n.array(data[:,0])*10
u = n.array(data[:,1])/1000
N = len(x)
# T0  = T[0]
# Tlog = n.log(T-Ta)
# pix = 18.9/66 # mm
# h   = data[1:,0]
herr = n.array([2]*N)
Cerr = u*0.03
# Terrlog = Terr/(T-Ta)

i = 5
#regression lineaire: fit_affine ou fit_linear
(a0, a_err, b0, b_err, chi2) = fit_affine(x[i:-i],     #abscisse
                                          u[i:-i],     #ordonnee
                                          herr[i:-i], #incertitude abscisse
                                          Cerr[i:-i]) #incertitude ordonnee

# # delta = -1/a0
# delta_err = a_err/a0**2
# T0mTa = n.exp(b0)

# print the results of the fit
print('    pente  = ' + '(%.5f +- %.5f)'%(a0,a_err) + unity + '/' + unitx + '\n')
print('    ordonnee  = ' + '(%.2f +- %.2f)'%(b0,b_err) + unity + '\n')
print('    chi2red  = ' + '%.2f  \n'%(chi2))

ploterr(size, mark, couleur,    #NE PAS TOUCHER
        x,                 #abscisse
        u,                 #ordonnee
        herr,                  #incertitude abscisse
        Cerr,                  #incertitude ordonnee
        ID   = 0               #numero du type de points
        )

#modelisation
plt.plot(np.linspace(0,x[-1],2),
         # T0mTa*n.exp(-x/delta) + Ta,
         b0 + a0*np.linspace(0,x[-1],2),
         color      = couleur[0],   #couleur de la courbe, mettre le numero voulu
#         label      = r'$\chi^2=%.2f$ '%(chi2)
         )
# #
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
figsave('udiff_vs_x')   #changer le nom de la figure
plt.show()

l=0.21
# Eff=10/np.sqrt(2)
Eff=5.74
mur=11
# print(mur)
print((1-1/mur)*Eff/l/2)
# print(Eff/2/l)
# mur=1/(1-a0*2*1000/Eff*l)
# print(mur)
# PENSER À ATTENDRE L'ÉQUILIBRE THERMIQUE DE L'EAU QUI CIRCULE !


# plot the graph of function x/(200-x)
# x = np.linspace(0,200,100)
# plt.plot(x,x/(400-x))
# plt.show()
