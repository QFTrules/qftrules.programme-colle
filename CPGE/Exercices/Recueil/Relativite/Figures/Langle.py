import numpy as np
import matplotlib.pyplot as plt

# Enable LaTeX rendering
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

def luminance(theta, beta):
    gamma = 1 / np.sqrt(1 - beta**2)
    return 1 / (gamma**2 * (1 - beta * np.cos(theta))**2)

theta = np.linspace(0, np.pi, 500)
beta = 0.5
L = luminance(theta, beta)

plt.figure(figsize=(5, 3.8))
plt.plot(theta, L, label=r'$\beta = {0}$'.format(beta))
plt.xlabel(r'$\theta$ (rad)')
plt.ylabel(r'Luminance')
# plt.title(r'Luminance as a function of $\theta$')
plt.legend()
plt.grid(True)
plt.xlim(0, np.pi)  # Set x-axis limits from 0 to π
plt.xticks([0,np.pi/4,np.pi/2,3*np.pi/4,np.pi],[r'0',r'$\pi/4$',r'$\pi/2$',r'$3\pi/4$',r'$\pi$'])
# plt.show()
plt.rcParams.update({'font.size': 14})
plt.savefig('Langle.pdf', bbox_inches='tight', pad_inches=0.1)