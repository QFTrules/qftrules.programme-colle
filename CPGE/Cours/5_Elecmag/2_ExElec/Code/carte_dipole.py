import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.rc('font',family='serif')
plt.rcParams.update({'font.size': 16})
plt.rc('text', usetex=True)
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'

X   = np.linspace(-2,2,201)
Y   = X
res = np.linspace(-5,5,20)
x,y = np.meshgrid(X,Y)
r = np.sqrt(x**2+y**2)
cos_theta = x/r
V   = cos_theta/r**2
# V = x/np.sqrt(x**2+y**2)**(3/2)
plt.figure(figsize=(5,5))
plt.xlim([-2,2])
plt.ylim([-2,2])
plt.yticks(np.arange(-2,3,1))
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')




Ex, Ey = np.gradient(V)
plt.streamplot(x,y,Ey,Ex, density=1, color='b')
plt.contour(x, y, V, res, colors = 'r', linestyles='solid')
plt.show()
