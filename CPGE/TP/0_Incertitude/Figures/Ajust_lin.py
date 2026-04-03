# -*- coding: utf-8 -*-

# import des bibliothèques python
from figure import *

# seuls les donnees experimentales et les labels sont a modifier
data=np.loadtxt('Ajust_lin.txt')
x = data[:,0]
y = data[:,1]

# incertitudes types
uy = 4.8  # 4.8 ou 1 ou 15
ux = 0.00001

(a0, a_err, b0, b_err, chi2) = fit_affine(x,     #abscisse
                                          y,     #ordonnee
                                          ux, #incertitude abscisse
                                          uy) #incertitude ordonnee


#print the results of the fit
print('courbe 1\n' +   '   pente    = %.5e +/- %.1e\n' %(a0, a_err)
      + '   ordonnee = %.3e +/- %.1e\n' %(b0, b_err)
      + '   chi2     = %.3f\n' % chi2)


### FIGURE ###

#dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize()

#creation figure
newfig()
ax = plt.gca()

#parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

#axe des abscisses
nmbx = 6            #nombre de traits
xmin = 0           #valeur minimale de x
xmax = 1.2           #valeur maximale de x

""" NE PAS TOUCHER """

# ax.set_xticks([0, 0.2, 0.4,0.6,0.8,1.0,1.2])
# plt.xlim([xmin, xmax])
# ax.set_xticklabels(['0,0', '0,2','0,4','0,6', '0,8', '1,0','1,2'])

""" FIN NE PAS TOUCHER """

#nom de la variable en abscisse
plt.xlabel(r'$x\ (\mathrm{unit\acute{e}\ arb.})$')

#petits traits intermediaires
# minorLocator = AutoMinorLocator(2)          #changer le nombre de petits traits
# ax.xaxis.set_minor_locator(minorLocator)    #a enlever si vous ne voulez pas de petits traits

#axe des ordonnees
nmby = 5
ymin = -2
ymax = 135

#si vous voulez l'echelle log
#plt.yscale('log')

""" NE PAS TOUCHER """

# plt.yticks([i for i in n.linspace(ymin,ymax,nmby)],
# 	[str(r'${}%.0f$'%(i)).replace('.',',') for i in n.linspace(ymin,ymax,nmby)])
plt.ylim(ymin, ymax)

""" FIN NE PAS TOUCHER """

#nom de la variable en ordonnee
plt.ylabel(r'$y\ (\mathrm{unit\acute{e}\ arb.})$')

#petits traits intermediaires
# ax.yaxis.set_minor_locator(minorLocator)

#points experimentaux
ploterr(size, mark, couleur,    #NE PAS TOUCHER
        x,                      #abscisse
        y,                 #ordonnee
        ux,                  #incertitude abscisse
        uy,                  #incertitude ordonnee
        ID   = 2,               #numero du type de points
        # name = r'donn\'{e}e 1'  #nom de la courbe, le r permet d'ecrire en latex
        )

#modelisation
plt.plot([np.min(x), np.max(x)],              #abscisse
         n.array([np.min(x), np.max(x)])*a0+b0,  #ordonnee
         color      = couleur[2],   #couleur de la courbe, mettre le numero voulu
        label      = r'$\chi^2_{\rm red}=\;$1,0'%(chi2)
         )

plt.legend()

#save the figure
figsave('Ajust_lin_2')   #changer le nom de la figure

plt.show()
