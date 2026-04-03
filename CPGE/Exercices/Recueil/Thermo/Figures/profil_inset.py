""" NE PAS TOUCHER """

# Module de base pour les figures
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
xmin = 0            # Valeur minimale de x
xmax = 240           # Valeur maximale de x


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

minorLocator = AutoMinorLocator(2)          # Nombre de sous-intervalles dilimites par les petits traits
ax.yaxis.set_minor_locator(minorLocator) 

# Nom de la variable en abscisse
plt.xlabel(r'$t$ (min)')

# Axe des ordonnees
nmby = 7
ymin = 100
ymax = 250

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
plt.ylabel(r'$h$ (mm)')

# Load the first set of data
data = n.loadtxt('diffusion_glycerol.txt',        # Nom du fichier avec les donnees
                 skiprows = 1)  # Pour sauter la premiere ligne
t    = data[:,0]*60              # Nom premiere variable
h    = n.array(data[:,1])/1000  # Nom deuxieme variable
N    = n.shape(t)[0]            # Taille de la liste
un_sur_h2 = 1/h**2

t_err = t*0 + 4
h_err = h*0 + n.sqrt(2)/1000

# Regression lineaire: fit_affine ou fit_linear
(a0, a_err, b0, b_err, chi2) = fit_affine(un_sur_h2,     # Abscisse
                                          t,     # Ordonnee
                                          h_err/h**3, # Incertitude abscisse
                                          t_err) # Incertitude ordonnee

# Print the results of the fit
print('courbe 1\n' +   '   pente    = %.3e +/- %.1e\n' %(a0, a_err)
      + '   ordonnee = %.3e +/- %.1e\n' %(b0, b_err)
      + '   chi2     = %.3f\n' % chi2)

# Points experimentaux
ploterr(size, mark, couleur,
		 t/60,            # Abscisse
         h*1000,                             # Ordonnee (ici je retranche l'origine des ordonnees par commodite mais c est juste pour l'exemple)
         t_err/60,           # Incertitude abscisse
         h_err/1000,           # Incertitude ordonnee
		 ID = 0)

# Modelisation. Attention plotcurve n'est pas la meme fonction que plt.plot !
plotcurve(size, mark, couleur,
		 n.linspace(1,300,100),              	  # Abscisse
         1000*n.sqrt(a0/(n.linspace(1,300,100)*60-b0)),  	  # Ordonnee
		 ID = 0)

# Legende
leg(sub,                # NE PAS TOUCHER
    'upper left')       # Position de la legende sur le qraphe

""" INSET """

# Creation de l'insert
ax_inset = inset_axes(sub,                      # NE PAS TOUCHER
                      width          = "40%",   # Largeur relative
                      height         = "40%",   # Hauteur relative
                      loc            = 1,       # Code pour la position
                      borderpad      = 1.5)       # Distance au cadre exterieur

#a% Axe des abscisses
nmbx = 6
xmin = 0
xmax = 100

# Memes remarques qu'au debut pour changer les axes
ax_inset.set_xticks(n.linspace(xmin, xmax, nmbx))
ax_inset.set_xticklabels([str('{}%.0f'%(i)).replace('.',',') for i in n.linspace(xmin,xmax,nmbx)])
ax_inset.set_xlim([xmin, xmax])
ax_inset.set_xlabel(r'$h^{-2}~$(m$^{-2}$)')

# Axe des ordonnes
nmby = 5
ymin = 0
ymax = 4
#ax_inset.set_yscale('log')

ax_inset.set_yticks(n.linspace(ymin, ymax, nmby))
ax_inset.set_yticklabels([str('{}%.0f'%(i)).replace('.',',') for i in n.linspace(ymin,ymax,nmby)])
ax_inset.set_ylim([ymin, ymax])
ax_inset.set_ylabel(r'$t~$(h)')

# Plot
inset_ploterr(ax_inset, size, mark, couleur,    #NE PAS TOUCHER
        un_sur_h2,                                      #abscisse
        t/3600,                                 #ordonnee
        h_err/h**3,                                  #incertitude abscisse
        t_err/3600,                                  #incertitude ordonne
        ID   = 0                                #numero du type de points
        )

inset_plotcurve(ax_inset, size, mark, couleur,    #NE PAS TOUCHER
        n.array([0,120]),                                      #abscisse
        (a0*n.array([0,120])+b0)/3600,                                 #ordonnee
        ID   = 0                                #numero du type de points
        )

# Save the figure
figsave('hauteur_vs_t_inset')   # Changer le nom de la figure
#plt.show()
