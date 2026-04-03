import numpy as np
import matplotlib.pyplot as pp



A=-.3
B=.8


def ech(y) :
    return (y-A)/(B-A)



pp.figure()

N=100
x = np.linspace(0,1,N)
a=.07
k=10


pp.ylim(A,B)
pp.xlim(0,1)


y = np.zeros(100)

maxi=.5

nb=40
for i in range(nb+1) :
    xi=float(i)/nb
    pp.axvline(x=xi,ymin=ech(0),ymax=ech(maxi),color="k")

pp.xticks([],[])
pp.yticks([],[])


nb=10
for i in range(nb+1):
    pp.plot(x,y+i*maxi/nb,color="k")

pp.show()


###############
# ondes S
###############


pp.figure()

N=100
x = np.linspace(0,1,N)
a=.07
k=10


pp.ylim(A,B)
pp.xlim(0,1)



def f(x) :
    return a*np.cos(k*x)


maxi=.5


nb=40
for i in range(nb+1) :
    xi=float(i)/nb
    pp.axvline(x=xi,ymin=ech(f(xi)),ymax=ech(maxi+f(xi)),color="k")

pp.xticks([],[])
pp.yticks([],[])


nb=10
for i in range(nb+1):
    pp.plot(x,f(x)+i*maxi/nb,color="k")



pp.show()


################
# ondes P
###############

pp.figure()

N=100
x = np.linspace(0,1,N)
a=.07
k=10



pp.ylim(A,B)
pp.xlim(0,1)


def f(x) :
    return a*np.cos(k*x)


maxi=.5


nb=40
for i in range(nb+1) :
    xi=float(i)/nb
    pp.axvline(x=xi+f(xi),ymin=ech(0),ymax=ech(maxi),color="k")

pp.xticks([],[])
pp.yticks([],[])


nb=10
for i in range(nb+1):
    pp.plot(x,np.zeros(N) + i*maxi/nb,color="k")



pp.show()

