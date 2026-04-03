import numpy as np
import matplotlib.pyplot as plt

def I(omega, E, R, L, C):
    omega_0 = 1 / np.sqrt(L * C)
    Q = omega_0 * R * C
    return (E / R) * np.sqrt(1 + Q**2 * ((omega / omega_0) - (omega_0 / omega))**2)

omega = np.linspace(0.1, 10, 100)
E = 1
R = 1
L = 1
C = 1

plt.plot(omega, I(omega, E, R, L, C))
plt.xlabel('x')
plt.ylabel('I(x)')
plt.grid(True)
plt.show()
plt.savefig('I_x.pdf')