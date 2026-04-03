"""             REGRESSION AFFINE               """
import numpy as np
import scipy.optimize as opt

# points expérimentaux
data = np.loadtxt('data.txt')                   # importation données tableau
X  = data[:0]                                   # absisse
Y  = data[:1]                                   # ordonnée
N  = len(X)                                     # nombre de points de mesure
DX = np.array([0.2]*N)                          # incertitude absisse
DY = np.array([2]*N)                            # incertitude ordonnée

# régression affine
def res(a,x,y):                                 # résidu
    return y-a[0]*x-a[1]
def resbis(a,x,y,dx,dy):                        # résidu avec incertitude
    return res(a,x,y)/np.sqrt(dy**2+a**2*dx**2)
p = opt.leastsq(resbis,                         # moindre carré
                    [1,0],                      # estimation de [a,b]
                    args = (X,Y,DX,DY),         # points expérimentaux
                    full_output = True)         # pour les incertitudes

# paramètres optimaux
a, b    = p[0]                                  # valeurs de a et b
Da, Db  = np.sqrt(np.abs(np.diagonal(p[1])))    # incertitudes-types
khi2red = sum(resbis([a,b],X,Y,DX,DY)**2)/(N-2) # valeur du khi2 reduit

print('    a  = ' + '%.1e +- %.1e  \n'%(a,Da))
print('    b  = ' + '%.1e +- %.1e  \n'%(b,Db))
print('    khi2red  = ' + '%.1e \n'%(khi2red))