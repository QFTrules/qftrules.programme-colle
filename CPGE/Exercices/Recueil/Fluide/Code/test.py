import numpy as np
import matplotlib.pyplot as plt

values_of_a = [1, 2, 3, 4, 5]  # Replace with your desired values of 'a'

theta = np.linspace(0, 2*np.pi, 100)

for a in values_of_a:
    r = a * abs(np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    plt.plot(x, y)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
plt.title("Lignes de courant")
plt.savefig('figure.pdf', dpi=300, format='pdf')
plt.axis('equal')  # Set equal aspect ratio for x and y axes
plt.show()
