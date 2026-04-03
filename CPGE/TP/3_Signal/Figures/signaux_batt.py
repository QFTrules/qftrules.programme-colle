""" NE PAS TOUCHER """

# Module de base pour les figures
from figure import *
from matplotlib.patches import FancyArrowPatch

# Dictionnaire pour les couleurs et points
(couleur, mark, size) = defsize(x=9)

# Creation de la figure
newfig()
ax = plt.gca()

# Parametres de la figure sont enregistres dans sub
sub = plt.subplot(1,1,1)

""" FIN NE PAS TOUCHER """

# Axe des abscisses 
nmbx = 6            # Nombre total de traits (i.e. nombres d'intervalles + 1)
xmin = 0            # Valeur minimale de x
xmax = 5           # Valeur maximale de x

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
plt.xlabel(r'$t$ (ms)')

# Petits traits intermediaires. NE PAS METTRE 0 DANS AutoMinorLocator, mais commenter la ligne pour les enlever.
minorLocator = AutoMinorLocator(2)          # Nombre de sous-intervalles dilimites par les petits traits
ax.xaxis.set_minor_locator(minorLocator)    # A enlever si vous ne voulez pas de petits traits

# Axe des ordonnees
nmby = 5
ymin = -2
ymax = 2

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
plt.ylabel(r'$U$ (V)')

# Petits traits intermediaires
ax.yaxis.set_minor_locator(minorLocator)

def sp(x):
    return 4*np.cos(10*2*np.pi*x) 
def si(x):
    return 2*np.sin(0.5*2*np.pi*x)
def s(x,k=0.1):
    return k*sp(x)*si(x)
# Load the first set of data
# data = n.loadtxt('test',        # Nom du fichier avec les donnees
#                  skiprows = 1)  # Pour sauter la premiere ligne
# t    = data[:,0]                # Nom premiere variable
# O    = data[:,1]                # Nom deuxieme variable
# N    = n.shape(t)[0]            # Taille de la liste

# # Load the second set of data
# data2 = n.loadtxt('test2',
#                   skiprows = 1)
# t2    = data2[:,0]
# O2    = data2[:,1]
# # N2    = n.shape(t2)[0]

# # Incertitudes. Je suppose qu'on travaille toujours avec les incertitudes-types (i.e. a 1 sigma)
# t_err   = n.zeros(N) + 0.2      # Mettre t/100 si 1% d'incertitude par ex.
# O_err   = n.zeros(N) + 0.3
# t_err2  = n.zeros(N2) + 0.2
# O_err2  = n.zeros(N2) + 0.3

# # Regression lineaire: fit_affine ou fit_linear
# (a0, a_err, b0, b_err, chi2) = fit_affine(t,     # Abscisse
#                                           O,     # Ordonnee
#                                           t_err, # Incertitude abscisse
#                                           O_err) # Incertitude ordonnee
                                          
# (a2, a_err2, b2, b_err2, chi2_2) = fit_affine(t2, O2, t_err2, O_err2)
# #(a, a_err, chi2) = fit_linear(t, O, t_err, O_err)

# # Print the results of the fit
# print('courbe 1\n' +   '   pente    = %.3e +/- %.1e\n' %(a0, a_err)
#       + '   ordonnee = %.3e +/- %.1e\n' %(b0, b_err)
#       + '   chi2     = %.3f\n' % chi2)

# print('courbe 2\n' +   '   pente    = %.3e +/- %.1e\n' %(a2, a_err2)
#       + '   ordonnee = %.3e +/- %.1e\n' %(b2, b_err2)
#       + '   chi2     = %.3f\n' % chi2_2)

# # Points experimentaux
# ploterr(size, mark, couleur,    # NE PAS TOUCHER
#         t,                      # Abscisse
#         O - b0,                 # Ordonnee (ici je retranche l'origine des ordonnees par commodite mais c est juste pour l'exemple)
#         t_err,                  # Incertitude abscisse
#         O_err,                  # Incertitude ordonnee
#         ID   = 0,               # Numero du type de points
#         name = r'donn\'{e}e 1'  # Nom de la courbe, le r permet d'ecrire en latex
#         )
        
# ploterr(size, mark, couleur,
#         t2, 
#         O2 - b2,
#         t_err2,
#         O_err2,
#         ID   = 1,
#         name = r'donn\'{e}e 2'
#         )

# # Je mets n importe quoi dans les ordonnees a titre d'exemple, bien entendu.
# ploterr(size, mark, couleur,
#         t2, 
#         O2*1.3 - b2,
#         t_err2,
#         O_err2,
#         ID   = 2,
#         name = r'donn\'{e}e 3'
#         )
             
# Modelisation. Attention plotcurve n'est pas la meme fonction que plt.plot !
X = np.linspace(xmin, xmax, 1000) # 1000 points pour la courbe
# plotcurve(size, mark, couleur,
# 	  X,              	  # Abscisse
#           sp(X),  	  # Ordonnee
#           ID   = 0,   			  # Index de la courbe, mettre le numero voulu
#           name = r'$s_p(t)$ ' # Nom de la courbe
#           )
         
# plotcurve(size, mark, couleur,
# 	  X,              	  # Abscisse
#           si(X),  	  # Ordonnee
#           ID   = 1,   			  # Index de la courbe, mettre le numero voulu
# #         name = r'$\chi^2=%.2f$ '%(chi2) # Nom de la courbe
#           name = r'$s_i(t)$ ' # Nom de la courbe

#           )
         
plotcurve(size, mark, couleur,
	  X,              	  # Abscisse
          s(X),   # Ordonnee
          ID   = 2,   			  # Index de la courbe, mettre le numero voulu
#         name = r'$\chi^2=%.2f$ '%(chi2) # Nom de la courbe
          name = r'$s(t)$ ' # Nom de la courbe

         )

# Legende
plt.legend(loc=(0,-0.03), ncol=3, facecolor='white', framealpha=1)  # NE PAS TOUCHER
# leg(sub,                # NE PAS TOUCHER
#     'upper left')       # Position de la legende sur le qraphe

# Draw double arrow to indicate period of wave

# Define the period of the wave
period = 1 / 0.5  # Since the frequency is 0.5 Hz for si(x)

# Coordinates for the double arrow
x_start = 1
x_end = 2
y_position = -1  # Position below the x-axis

# Draw the double arrow
arrow = FancyArrowPatch((x_start, y_position), (x_end, y_position), 
                        arrowstyle='<->', mutation_scale=10, color='black')
ax.add_patch(arrow)

# Add text to indicate the period
plt.text((x_start + x_end) / 2, y_position - 0.2, r'$1/\delta f$', 
         horizontalalignment='center', verticalalignment='center')

# Save the figure
figsave('signaux')   # Changer le nom de la figure

