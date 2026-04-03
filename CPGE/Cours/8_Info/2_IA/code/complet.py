import random as r
import matplotlib.pyplot as plt
#import figure as fig
import matplotlib as mpl
import numpy as np
Fsize   = int(20)     # Big size, which corresponds to the size of the legend in latex (/small)
fsize   = int(15)     # Small size, eventually for the marks but we use the same value finally
""" LATEX ENVIRONEMENT """
pgf_with_latex = {                       # Setup matplotlib to use latex for output
    "pgf.texsystem":   "pdflatex",       # Change this if using xetex or lautex
    "text.usetex":     True,             # Use LaTeX to write all text
    "font.family":     "serif",
    "font.serif":      [],               # Blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace":  [],
    "axes.labelsize":  Fsize,            # Here is the default font size (10pt, 11pt or 12pt typically)
    "font.size":       Fsize,
    "legend.fontsize": Fsize,            # Make the legend/label fonts a little smaller
    "xtick.labelsize": fsize,
    "ytick.labelsize": fsize,
    "pgf.preamble": r"\usepackage[utf8x]{inputenc}\usepackage[T1]{fontenc}"
}

# Set the new params to default
mpl.rcParams.update(pgf_with_latex)

# add grid

def partition(E, k, centres, d):
    p = dict()                   # initialisation de la partition, dictionnaire vide
    for x in E:
        c    = min(centres, key = lambda y:d(x,y))  # centre le plus proche de x
        p[x] = centres.index(c)                     # classe attribuée à x
    return p

def couleur(p):
    col = ['','','']
    for i in range(3):
        x = [f[0] for f in p if p[f] == i]
        y = [f[1] for f in p if p[f] == i]
        if 0 < np.mean(y) and np.mean(y) < 150/250 and not 'r' in col:
            col[i] = 'og'
        elif 50/250 < np.mean(y) and np.mean(y) < 200/250 and not 'y' in col:
            col[i] = 'sy'
        else:
            col[i] = '^r'
    return col

def graph(p,j,col,c,centre=True):
    x = [f[0] for f in p]
    y = [f[1] for f in p]


    # # Dictionnaire pour les couleurs et points
    # (couleur, mark, size) = defsize()

    # Creation de la figure
    #newfig()
    plt.figure(figsize=(6*1.618,6))
    plt.grid()
    
    #ax = plt.gca()

    # # Parametres de la figure sont enregistres dans sub
    # sub = plt.subplot(1,1,1)
    #
    # """ FIN NE PAS TOUCHER """
    #
    # minorLocator = AutoMinorLocator(3)          # Nombre de sous-intervalles dilimites par les petits traits
    # ax.xaxis.set_minor_locator(minorLocator)
    #
    # Axe des abscisses
    nmbx = 12           # Nombre total de traits (i.e. nombres d'intervalles + 1)
    xmin = 0.45            # Valeur minimale de x
    xmax = 1           # Valeur maximale de x


    """ NE PAS TOUCHER """

    plt.xticks([ i for i in np.linspace(xmin,xmax,nmbx)],
        [str('{}%.2f'%(i)).replace('.',',') for i in np.linspace(xmin,xmax,nmbx)]) # Ici vous pouver changer le nombre de decimales (.0f)
    plt.xlim([xmin, xmax])

    """
    REMARQUE:
    Pour le nombre de decimales, il est conseille d'en mettre le minimum possible afin d'alleger le graphe.
    .0f correspond a des entiers, .1f a un flottant avec un chiffre apres la virgule, etc.

    """

    """ FIN NE PAS TOUCHER """
    # Nom de la variable en abscisse
    plt.xlabel(r'masse normalisée')

    # Axe des ordonnees
    nmby = 12
    ymin = 0.45
    ymax = 1

    # Si vous voulez l'echelle log
    #plt.yscale('log')

    # Si vous avez besoin de mettre les axes origines
    #ax.axhline(y=0, color='k', linewidth = 0.2)
    #ax.axvline(x=0, color='k', linewidth = 0.2)

    """ NE PAS TOUCHER """

    plt.yticks([i for i in np.linspace(ymin,ymax,nmby)],
    	[str('{}%.2f'%(i)).replace('.',',') for i in np.linspace(ymin,ymax,nmby)]) # Ici vous pouver changer le nombre de decimales (.0f)
    plt.ylim([ymin, ymax])

    """ FIN NE PAS TOUCHER """

    # Nom de la variable en ordonnee
    plt.ylabel(r'couleur')

    for i in range(3):
        x = [f[0] for f in p if p[f] == i]
        y = [f[1] for f in p if p[f] == i]
        plt.plot(x,y,col[i], markersize=7)
        # if centre:
            # plt.plot(c[i][0],c[i][1],'D' + col[i], markersize=7, markeredgecolor='black')

    plt.savefig('fruits_%i.pdf'%j)

def bary(points):
    D = len(points[0])      # dimension de l’espace affine
    b = [0]*D               # initialisation du barycentre
    N = len(points)         # nombre d’éléments
    for x in points:        # boucle sur les points
        for i in range(D):          # boucle sur coordonnées
            b[i] = b[i] + x[i]/N    # addition  divisée par N
    return b                        # barycentre

def moy(E, k, d, ni):
    c = r.sample(E, k)                    # centres aléatoires
    p = partition(E, k, c, d)       # partionnement autour des centres
    graph(p,-1,['b','b','b'],c,centre=False)
    color = couleur(p)
    for j in range(ni):                 # itération du partionnement
        p = partition(E, k, c, d)       # partionnement autour des centres
        graph(p,j,color,c)
        for i in p.values():                     # boucle sur classe i
            classe = [x for x in p if p[x] == i] # ensemble correspondant
            c[i]   = bary(classe)                # ré-évaluation centres
    return p, c                         # retourne partition et centres

def tomate():
    m = 100 + r.randrange(-25,25)
    v = 50 + r.randrange(-50,50)
    return m/150,0.45+0.55*(1-v/250)
def banane():
    m = 130 + r.randrange(-25,25)
    v = 160 + r.randrange(-50,50)
    return m/150,0.45+0.55*(1-v/250)
def kiwi():
    m = 90 + r.randrange(-15,15)
    v = 220 + r.randrange(-20,20)
    return m/150,0.45+0.55*(1-v/250)

def fruits(N):
    E = []
    for i in range(N):
        fruit = r.randrange(3)
        if fruit == 0:
            E.append(tomate())
        if fruit == 1:
            E.append(banane())
        if fruit == 2:
            E.append(kiwi())
    return E

def d(x, y):
    return ((y[0]-x[0])/150)**2 + ((y[1]-x[1])/255)**2

E    = fruits(100)
p, c = moy(E, 3, d, 20)
