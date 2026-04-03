"""
Vous pouvez modifier ce code pour l'adapter à vos besoins.
"""
# BIBLIOTHÈQUES
import matplotlib.pyplot as plt
import numpy as np

""" QUESTION 4 """

""" PARAMÈTRES PHYSIQUES """
g     = 9.8 # accélération de la pesanteur (en m.s^-2)
Tsideral = 1   # À MODIFIER
latitude = 0   # À MODIFIER
L        = 1   # À MODIFIER
omega0   = 1   # À MODIFIER
T0       = 1   # À MODIFIER

""" QUESTION 5 """

t = np.linspace(0,10*T0,1000) # tableau des instants de tracé
v0 = 1  # À MODIFIER   
x0 = 1  # À MODIFIER
x = 0*t #  À MODIFIER
y = 0*t #  À MODIFIER

""" TRACÉ """
plt.figure()
plt.xlim(-1.5*x0,1.5*x0)
plt.ylim(-1.5*x0,1.5*x0)
plt.xlabel('x')
plt.ylabel('y')
plt.plot(x,y)
plt.show()

""" QUESTION 6 """

dt = 0.01 # pas de temps
x = np.zeros(1000) # tableau des abscisses
y = np.zeros(1000) # tableau des ordonnées

def x_i_plus_1(x_i,x_i_moins_1,y_i,y_i_moins_1):
    return 0*x_i

def y_i_plus_1(x_i,x_i_moins_1,y_i,y_i_moins_1):
    return 0*y_i

for i in range(1,999):
    x[i+1] = x_i_plus_1(x[i],x[i-1],y[i],y[i-1])
    y[i+1] = y_i_plus_1(x[i],x[i-1],y[i],y[i-1])

""" TRACÉ """
plt.figure()
plt.xlim(-1.5*x0,1.5*x0)
plt.ylim(-1.5*x0,1.5*x0)
plt.xlabel('x')
plt.ylabel('y')
plt.plot(x,y)
plt.show()