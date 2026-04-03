def d(x, y):
    return (y[0]-x[0])**2 + (y[1]-x[1])**2

import matplotlib as mpl     					# Ici on importe matplotlib pour definir les fonctions de trace

Fsize =15
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

from random import sample
import numpy as np
def centres(E, k):
    return sample(E, k)  # k éléments distincts de E

def moy(E, k, d, ni):
    c = sample(E, k)                    # centres aléatoires
    for j in range(ni):                 # itération du partionnement
        p = partition(E, k, c, d)       # partionnement autour des centres
        show_fig(E,c,p,j)
        for i in p.values():                     # boucle sur classe i
            classe = [x for x in p if p[x] == i] # ensemble correspondant
            c[i]   = bary(classe)                # ré-évaluation centres
    return p, c                         # retourne partition et centres

def partition(E, k, centres, d):
    """
    Entrée : ensemble d’apprentissage E (list), nombre de moyennes k (int),
             centres de classe centres (list), distance d (function)
    Action : partitionne E autour des centres selon la distance d
    Sortie : partition p (dict)
    """
    p = dict()                   # initialisation de la partition, dictionnaire vide
    # print(centres)
    for x in E:
        c    = min(centres, key = lambda y:d(x,y))  # centre le plus proche de x
        # print(c)
        p[x] = centres.index(c)                     # classe attribuée à x
    return p


def bary(points):
    D = len(points[0])      # dimension de l’espace affine
    (xb,yb) = (0,0)               # initialisation du barycentre
    N = len(points)         # nombre d’éléments
    for x in points:        # boucle sur les points
        # for i in range(D):      # boucle sur coordonnées
        xb = xb + x[0]/N  # addition
        yb = yb + x[1]/N  # addition
    return (xb,yb)                  # somme divisée par N = barycentre

E=[(0.22, 0.46), (0.23, 0.53), (0.27, 0.59), (0.27, 0.42), (0.27, 0.5), (0.3, 0.55), (0.3, 0.49), (0.31, 0.39), (0.32, 0.46), (0.33, 0.31), (0.34, 0.44), (0.34, 0.41), (0.34, 0.36), (0.35, 0.56), (0.35, 0.5), (0.36, 0.63), (0.36, 0.46), (0.38, 0.56), (0.38, 0.62), (0.38, 0.4), (0.38, 0.44), (0.38, 0.49), (0.4, 0.52), (0.41, 0.47), (0.41, 0.34), (0.41, 0.54), (0.42, 0.41), (0.43, 0.59), (0.43, 0.66), (0.43, 0.52), (0.44, 0.49), (0.44, 0.4), (0.44, 0.45), (0.44, 0.32), (0.45, 0.58), (0.46, 0.48), (0.46, 0.4), (0.47, 0.36), (0.48, 0.51), (0.48, 0.62), (0.49, 0.57), (0.49, 0.42), (0.49, 0.55), (0.5, 0.34), (0.5, 0.48), (0.5, 0.5), (0.5, 0.66), (0.51, 0.58), (0.51, 0.46), (0.52, 0.67), (0.54, 0.41), (0.55, 0.36), (0.55, 0.53), (0.56, 0.51), (0.56, 0.4), (0.56, 0.63), (0.56, 0.58), (0.01, 0.85), (0.01, 0.72), (0.02, 0.88), (0.06, 0.68), (0.06, 0.75), (0.07, 0.89), (0.08, 0.79), (0.08, 0.77), (0.09, 0.84), (0.09, 0.93), (0.09, 0.81), (0.11, 0.81), (0.11, 0.63), (0.11, 0.75), (0.12, 0.87), (0.15, 0.89), (0.15, 0.7), (0.15, 0.85), (0.17, 0.72), (0.17, 0.97), (0.18, 0.9), (0.19, 0.85), (0.21, 0.88), (0.21, 0.78), (0.21, 0.64), (0.21, 0.99), (0.22, 0.9), (0.23, 0.86), (0.24, 0.7), (0.23, 0.53), (0.25, 0.74), (0.25, 0.78), (0.26, 0.92), (0.26, 0.89), (0.27, 0.59), (0.28, 0.79), (0.28, 0.88), (0.29, 0.65), (0.3, 0.93), (0.3, 0.49), (0.31, 0.84), (0.31, 0.79), (0.31, 0.39), (0.32, 0.46), (0.33, 0.69), (0.33, 0.31), (0.34, 0.41), (0.35, 0.56), (0.35, 0.5), (0.36, 0.63), (0.36, 0.46), (0.38, 0.56), (0.38, 0.61), (0.38, 0.44), (0.38, 0.49), (0.41, 0.47), (0.41, 0.34), (0.41, 0.54), (0.42, 0.41), (0.43, 0.59), (0.43, 0.66), (0.43, 0.52), (0.44, 0.49), (0.44, 0.4), (0.46, 0.48), (0.46, 0.4), (0.47, 0.36), (0.48, 0.62), (0.5, 0.34), (0.5, 0.48), (0.5, 0.66), (0.5, 0.5), (0.52, 0.67), (0.54, 0.41), (0.55, 0.36), (0.55, 0.53), (0.56, 0.51), (0.56, 0.4), (0.56, 0.63), (0.58, 0.15), (0.62, 0.31), (0.63, 0.23), (0.64, 0.06), (0.69, 0.37), (0.7, 0.27), (0.7, 0.16), (0.71, 0.1), (0.71, 0.22), (0.74, 0.14), (0.75, 0.01), (0.76, 0.2), (0.77, 0.08), (0.78, 0.27), (0.79, 0.15), (0.79, 0.19), (0.81, 0.05), (0.83, 0.3), (0.84, 0.22), (0.84, 0.08), (0.85, 0.13), (0.87, 0.02), (0.87, 0.19), (0.88, 0.22), (0.88, 0.1), (0.89, 0.34), (0.89, 0.05), (0.89, 0.27), (0.89, 0.14), (0.9, 0.19), (0.92, 0.15), (0.92, 0.06), (0.93, 0.2), (0.93, 0.26), (0.95, 0.28), (0.98, 0.17), (0.02, 0.22), (0.03, 0.16), (0.07, 0.17), (0.08, 0.26), (0.09, 0.14), (0.1, 0.1), (0.1, 0.3), (0.11, 0.16), (0.11, 0.22), (0.12, 0.11), (0.12, 0.07), (0.14, 0.24), (0.14, 0.03), (0.15, 0.18), (0.15, 0.11), (0.16, 0.03), (0.18, 0.22), (0.18, 0.28), (0.18, 0.02), (0.19, 0.09), (0.19, 0.15), (0.2, 0.21), (0.2, 0.05), (0.21, 0.01), (0.21, 0.19), (0.22, 0.28), (0.22, 0.11), (0.22, 0.22), (0.22, 0.14), (0.23, 0.36), (0.25, 0.11), (0.25, 0.03), (0.25, 0.26), (0.26, 0.18), (0.27, 0.15), (0.27, 0.34), (0.28, 0.1), (0.28, 0.21), (0.28, 0.13), (0.29, 0.05), (0.3, 0.09), (0.3, 0.0), (0.3, 0.27), (0.31, 0.15), (0.33, 0.06), (0.34, 0.13), (0.34, 0.03), (0.36, 0.14), (0.37, 0.09), (0.38, 0.27), (0.38, 0.21), (0.58, 0.46), (0.58, 0.59), (0.6, 0.65), (0.64, 0.56), (0.64, 0.48), (0.66, 0.64), (0.66, 0.72), (0.68, 0.69), (0.68, 0.77), (0.68, 0.47), (0.7, 0.67), (0.71, 0.65), (0.71, 0.49), (0.71, 0.75), (0.71, 0.69), (0.71, 0.56), (0.73, 0.73), (0.73, 0.65), (0.74, 0.69), (0.73, 0.6), (0.75, 0.53), (0.75, 0.82), (0.75, 0.59), (0.76, 0.61), (0.76, 0.65), (0.76, 0.51), (0.76, 0.32), (0.77, 0.67), (0.77, 0.58), (0.77, 0.75), (0.78, 0.8), (0.78, 0.63), (0.79, 0.73), (0.81, 0.8), (0.81, 0.48), (0.82, 0.7), (0.82, 0.73), (0.83, 0.62), (0.84, 0.67), (0.84, 0.76), (0.84, 0.53), (0.85, 0.7), (0.85, 0.58), (0.85, 0.44), (0.86, 0.62), (0.86, 0.64), (0.87, 0.71), (0.87, 0.57), (0.88, 0.66), (0.88, 0.68), (0.89, 0.6), (0.89, 0.51), (0.9, 0.56), (0.9, 0.63), (0.96, 0.6), (0.96, 0.68), (0.96, 0.55)]
print(len(E))

def show_fig(E,c,p,j):
    # Extract x and y coordinates from E and c
    E_x = [point[0] for point in E]
    E_y = [point[1] for point in E]
    c_x = [point[0] for point in c]
    c_y = [point[1] for point in c]

    # Plotting the points
    for i, point in enumerate(E):
        if p[point] == 1:
            plt.scatter(point[0], point[1], color='red', label='p=1')
        elif p[point] == 2:
            plt.scatter(point[0], point[1], color='blue', label='p=2')
        elif p[point] == 3:
            plt.scatter(point[0], point[1], color='green', label='p=3')
        elif p[point] == 4:
            plt.scatter(point[0], point[1], color='orange', label='p=4')
        elif p[point] == 0:
            plt.scatter(point[0], point[1], color='purple', label='p=5')

    # Plotting the centers
    plt.scatter(c_x, c_y, color='black', label='c', marker='*')
    # plt.scatter(0.37,0.69, color='black', label='x', marker='<')

    # Adding labels and legend
    plt.xlabel('$e$')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.ylabel('$n$')
    plt.yticks(np.arange(0, 1.1, 0.1))
    # plt.legend()
    plt.savefig('kmeans_%i_k3.pdf'%j)
    # Display the graph
    # plt.show()
    plt.close()

p, c = moy(E, 3, d, 11)
print(p,c)
import matplotlib.pyplot as plt
