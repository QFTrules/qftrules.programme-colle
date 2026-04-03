
"""
IMPORTANT !!!!
Ce fichier doit toujours etre nomme figure.py
Il est a placer dans le repertoire python qui contient la liste des bibliotheques,
ou dans le dossier courant ou sont vos programmes python.
Pour trouver le dossier contenant les bibliotheques, choisissez un des dossiers
que vous sort la commande:
	>>> import sys
	>>> sys.path
dans une shell python. Il peut etre necessaire de relancer ensuite la console python
pour que le module soit bien trouve.
"""

""" PACKAGES """

import numpy as n	     					# Ici on importe numpy parce qu'il sert tout le temps
from scipy import *	     					# Pour certains calculs
# from pylab import *	     					# Pour certains calculs

import matplotlib as mpl     					# Ici on importe matplotlib pour definir les fonctions de trace
import matplotlib.pyplot as plt 				# Idem
#mpl.use("pgf")              					# Import pgf package for output figure (not necessary because we will use pdf)

import scipy.optimize as opt 					# Pour la modelisation


from matplotlib.ticker import AutoMinorLocator			# Pour les ticks sur les axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes	# Pour les inserts

""" RC PARAMETERS """

mpl.rc('legend',
       numpoints     = 1,     # The number of marker points in the legend line
       handletextpad = 0.3,   # The space between the legend line and legend text
       handlelength  = 0.7,   # The length of the legend lines
       borderpad     = 0.7,   # Border whitespace
       columnspacing = 0.8,   # Column separation
       frameon       = False)  # If True, draw the legend on a background patch

mpl.rc('axes',
       linewidth = 0.5,       # Edge linewidth
       grid      = False)     # Grille

mpl.rc('lines',
       markeredgewidth = 0,   # The line width around the marker symbol
       linewidth       = 0.5, # Line width in points
       linestyle       = '-', # Default line style
       markersize      = 0)   # No markersize by default

mpl.rc('xtick.major',
       size  = 2.2,           # Major tick size in points
       pad   = 3,             # Distance to major tick label in points
       width = 0.5)           # Major tick width in points

mpl.rc('xtick.minor',         # Smaller ticks
       size = 1.1,
       pad  = 3,
       width = 0.5)

mpl.rc('ytick.major',         # Idem for y
       size = 2.2,
       pad  = 3,
       width = 0.5)

mpl.rc('ytick.minor',
       size = 1.1,
       pad  = 3,
       width = 0.5)

""" FIGURE SIZE """

def figsize(scale):                                 # Define default ratio
    fig_width_pt =  341.43307                       # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (n.sqrt(5.0)-1.0)/2.0             # The golden number is an aesthetic ratio
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

# Fonts and markers
def defsize(x = 10):	      # x is the font size of the latex document
    Fsize   = int(x*9/10)     # Big size, which corresponds to the size of the legend in latex (/small)
    fsize   = int(x*9/10)     # Small size, eventually for the marks but we use the same value finally

    # List of colors, markers and markersizes
    couleur = [[0,0.55,0.55] , [0.86,0.08,0] , [0.15, 0.6, 0.0] , [1.0, 0.75, 0.0] , [0.52, 0.52, 0.51] ]
    mark    = ['o'           , '^'           , 's'              , 'D'              , '<'                ]
    size    = [(7.*fsize)/20  , (8.*fsize)/20  , (7.*fsize)/20  , (7.*fsize)/20    , (9.*fsize)/20      ]

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
        "xtick.labelsize": Fsize,
        "ytick.labelsize": Fsize,
        "pgf.preamble": r"\usepackage[utf8x]{inputenc}\usepackage[T1]{fontenc}"
    }

    # Set the new params to default
    mpl.rcParams.update(pgf_with_latex)

    # Return the list of the marker properties
    return (couleur, mark, size)


""" FIGURE FUNCTIONS """

# Resolution in dots per inch
res = 200

# Creation of a new figure
def newfig(scale = 0.75):

    # Ajouter plt.clf() pour nettoyer la fenetre graphique
    plt.figure(figsize = figsize(scale), dpi = res)

""" LEGEND
Le but de cette fonction ci-dessous est de modifier certaines proprietes de base
de la legende qui ne sont pas ouf dans python, comme la presence de deux points au
loin d'un seul, ou encore pour changer l'epaisseur des petits traits
"""
def leg(sub, position):

    # Get handles
    handles, labels = sub.get_legend_handles_labels()
    h = []

    # Remove the errorbars
    for H in handles:
        try:
            h.append(H[0])
        except(TypeError):
            h.append(H)

    # Definition de la legende
    lege = plt.legend(h, labels, loc = position)

    # Epaisseur des lignes
    for line in lege.get_lines():
        line.set_linewidth(0.5)


""" PLOT """

# Plot with points and errorbars
def ploterr(size, mark, couleur, x, y, x_err, y_err, ID = 0, name = ''):
    plt.errorbar(x,
                 y,
                 xerr       = x_err,
                 yerr       = y_err,
                 markersize = size[ID],
                 marker     = mark[ID],
                 color      = couleur[ID],
                 linestyle  = '',
                 capsize    = 0,
                 elinewidth = 0.3,
                 label      = name
                 )

# Plot for plain curves, like theoretical models
def plotcurve(size, mark, couleur, x, y, ID = 0, name = ''):
    plt.plot(x, 
             y,
             marker     = mark[ID],
             color      = couleur[ID], 
             label      = name
             )

# Idem for inset plots
def inset_ploterr(ax_inset, size, mark, couleur, x, y, x_err, y_err, ID = 0, name = ''):
    ax_inset.errorbar(x,
                      y,
                      xerr       = x_err,
                      yerr       = y_err,
                      markersize = size[ID],
                      marker     = mark[ID],
                      color      = couleur[ID],
                      linestyle  = '',
                      capsize    = 0,
                      elinewidth = 0.3,
                      label      = name
                     )

# Plot for plain curves, like theoretical models
def inset_plotcurve(ax_inset, size, mark, couleur, x, y, ID = 0, name = ''):
    ax_inset.plot(x, 
             	  y,
             	  marker     = mark[ID],
             	  color      = couleur[ID], 
             	  label      = name
             	  )

""" SAVE FIGURE """

# Paths
pgfpath = ''
auxpath = ''

# Save the figure
def figsave(filename, path1 = pgfpath, path2 = auxpath):

    # pgf output
    #plt.savefig(path1 + '{}.pgf'.format(filename),
    #            bbox_inches = 'tight',    # removes all of the extra white space around the figure
    #            pad_inches  = 0.05,       # space around the frame for axis variables
    #            dpi         = res)        # resolution

    # pdf output
    plt.savefig(path2 + '{}.pdf'.format(filename),
                bbox_inches = 'tight',
                pad_inches  = 0.05,
                dpi         = res)

    # eps output
    #plt.savefig(path2 + '{}.eps'.format(filename),
    #            bbox_inches = 'tight',
    #            pad_inches  = 0.05,
    #            dpi         = res)

""" FIT FUNCTIONS """

# fit_affine() realise un ajustement affine des donnes avec incertitudes, po = estimation initiale
def fit_affine(x,y,dx,dy, p0 = n.array([0,0])):

    # Nombre de parametres
    N = n.shape(x)[0]

    # Residual est la fonction dont la somme des carres donne le chi2
    def residual(a,x,y,dx,dy):
        return (y-a[0]*x-a[1])/n.sqrt(dy**2 + (a[0]*dx)**2)    

    # Output de la fonction de minimisation du chi2
    result         = opt.leastsq(residual, p0, args = (x,y,dx,dy), full_output = True)

    # Meilleur estimation des parametres
    (a0, b0)       = result[0]


    # Incertitudes sur les parametres
    (a_err, b_err) = n.sqrt(n.abs(n.diagonal(result[1])))

    # Valeur du chi2 reduit
    chi2           = sum(residual([a0,b0],x,y,dx,dy)**2)/(N-2)

    # Retourne les parametres et le chi2
    return (a0, a_err, b0, b_err, chi2)

# fit_linear() realise un ajustement lineaire des donnes avec incertitudes, po = estimation initiale
def fit_linear(x,y,dx,dy, p0 = n.array([0])):

    # Nombre de parametres
    N = n.shape(x)[0]

    # Residual est la fonction dont la somme des carres donne le chi2
    def residual(a,x,y,dx,dy):
        return (y-a*x)/n.sqrt(dy**2 + (a*dx)**2)

    # Output de la fonction de minimisation du chi2
    result = opt.leastsq(residual, p0, args = (x,y,dx,dy), full_output = True)

    # Meilleur estimation des parametres
    a0     = result[0]

    # Incertitudes sur les parametres
    a_err  = n.sqrt(n.abs(n.diagonal(result[1])))

    # Valeur du chi2 reduit
    chi2   = sum(residual(a0,x,y,dx,dy)**2)/(N-2)

    # Retourne les parametres et le chi2
    return (a0, a_err, chi2)
