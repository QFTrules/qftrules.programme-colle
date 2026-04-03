import sympy
from sympy.abc import x, y
import numpy as np
import matplotlib.pyplot as plt

def potentiel(U=1, R=1): #potentiel des vitesses
    r       = sympy.sqrt(x**2 + y**2) #conversion polaires/cartésiennes
    theta   = sympy.atan2(y, x)
    return U * r *(1+0.5*(R/r)**3)* sympy.cos(theta) #expression potentiel

def vitesse(phi): #on dérive le potentiel pour avoir la vitesse
    u = sympy.lambdify((x, y), phi.diff(x), 'numpy')
    v = sympy.lambdify((x, y), phi.diff(y), 'numpy')
    return u, v

def plot_streamlines(ax, u, v, xlim=(-3, 3), ylim=(-3, 3)): #tracé des lignes de courant
    x0, x1  = xlim
    y0, y1  = ylim
    Y, X    = np.ogrid[y0:y1:100j, x0:x1:100j]
    ax.streamplot(X, Y, u(X, Y), v(X, Y), color='blue', integration_direction='both',
                  start_points=[[0,i/5] for i in range(-15,-4)])

def format_axes(ax):
    ax.set_aspect('equal')
    ax.figure.subplots_adjust(bottom=0, top=1, left=0, right=1)
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    for spine in ax.spines.itervalues():
        spine.set_visible(False)

import matplotlib as mpl
plt.rc('font',family='serif')
plt.rcParams.update({'font.size': 15})
plt.rc('text', usetex=True)
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'

phi = potentiel()
u, v = vitesse(phi)

#tracé
fig, ax = plt.subplots(figsize=(6,6))
plot_streamlines(ax, u, v)
circle = plt.Circle((0, 0), radius=1, color='k',fill='True') #ajout sphère noire de rayon R=1
plt.gca().add_patch(circle)
plt.xlabel('$x$')
plt.xlim(-3,3)
plt.ylabel('$y$')
plt.ylim(-3,3)
plt.show()
#fig.savefig('ecoulement_sphere.pdf',bbox_inches='tight')
