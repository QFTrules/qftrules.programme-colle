# <codecell>
import numpy as np
N    = 2**12     # Nombre de valeurs de k et de x
xmin = -10       # valeur minimale de x
xmax = 10        # valeur maximale de x
L    = xmax-xmin # Longueur de l'intervalle
X    = np.linspace(xmin, xmax, N)   # tableau des x
k    = np.linspace(0,2*np.pi*N/L,N) # tableau des k

k0     = 6
deltak = 1
A      = np.array([np.exp(-((k[i]-k0)/deltak)**2) for i in range(N)])

# <codecell>
# Tracé du spectre
import matplotlib.pyplot as plt
plt.figure()
plt.plot(k, np.abs(A))
plt.xlim([0,20])
plt.xlabel('k')
plt.ylabel('A(k)')
plt.show()
plt.close()

# <codecell>
def s_ini(k, X, A):
    s = np.zeros(len(X), dtype=np.complex_)
    for i in range(len(k)):
        s += np.array(A[i]) * np.exp(1j * k[i] * X)
    return np.real(s)

s0 = s_ini(k, X, A)
plt.figure()
plt.plot(X, s0)
plt.ylabel('s(x,t=0)')
plt.xlabel('x')
plt.show()
plt.close()

# <codecell>
def omega(k):
    omegap = 5
    c = 1
    return (k**2*c**2+omegap**2)**0.5

def s_temps(k, X, A, t):
    s = np.zeros(len(X), dtype=np.complex_)
    for i in range(len(k)):
        s += np.array(A[i]) * np.exp(1j * k[i] * X) * np.exp(-1j * omega(k[i]) * t)
    return np.real(s)

t = 7
st = s_temps(k, X, A, t)
plt.figure()
plt.plot(X, s0, color='b')
plt.plot(X, st, color='r')
plt.xlabel('x')
plt.ylabel('s(x,t)')
plt.show()
plt.close()
