from random import random
N = 100
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
