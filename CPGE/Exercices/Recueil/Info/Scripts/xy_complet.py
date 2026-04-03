from random import random
N = 1000
E = [(2*random()-1,2*random()-1) for i in range(N)]

import matplotlib.pyplot as plt
x = [x for x,y in E]
y = [y for x,y in E]
plt.plot(x,y,'d')
plt.show()

def d(x, y):
    return (y[0]-x[0])**2 + (y[1]-x[1])**2

def couleur(y, d):
    if d(y,(0,0)) < 0.5:
        return 'rouge'
    else:
        return 'bleu'

p  = {y:couleur(y,d) for y in E}

xr = [y[0] for y in E if p[y]=='rouge']
yr = [y[1] for y in E if p[y]=='rouge']
xb = [y[0] for y in E if p[y]=='bleu']
yb = [y[1] for y in E if p[y]=='bleu']
plt.plot(xr,yr,'rd')
plt.plot(xb,yb,'bd')
plt.show()

def tri(E, x, d):
  return sorted(E, key = lambda y:d(x,y))  # tri selon la distance de y à x

def voisins(E, x, d, k):
    liste = tri(E, x, d)                # liste triée (y,distance)
    return liste[:k]                    # k points y les plus proches

def classe(E, x, d, k, p):
    v = voisins(E, x, d, k)             # k plus proches voisins de x
    c = {p[y]:0 for y in v}             # liste des classes des voisins
    for y in v:                         # boule sur voisins
        c[p[y]] += 1                    # comptage des classes
    maxi = 0                            # initialisation maximum
    for i in c:                         # boucle sur classes des voisins
        if c[i] > maxi:                 # si classe i plus nombreuse
            maxi, classmaj = c[i], i    # mise à jour classe majoritaire
    return classmaj                     # retourne classe majoritaire

x = (0.71,0)
print(classe(E, x, d, 1, p))
print(classe(E, x, d, 3, p))
print(classe(E, x, d, 7, p))
plt.plot(xr,yr,'rd')
plt.plot(xb,yb,'bd')
plt.plot(x[0],x[1],'gd')
plt.show()
