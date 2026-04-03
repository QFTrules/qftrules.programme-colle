import numpy as np
from scipy.special import jv

import matplotlib.pyplot as plt

# Enable LaTeX rendering for the tick labels
plt.rcParams['text.usetex'] = True
plt.rcParams['xtick.labelsize'] = 14  # Set the font size for x-axis tick labels
plt.rcParams['ytick.labelsize'] = 14  # Set the font size for y-axis tick labels

# Define the x-axis values
x = np.linspace(0, 20, 100)


# Plot a black horizontal line for zero
plt.axhline(0, color='black')

y = jv(0, x)  # Calculate the Bessel function values
plt.plot(x, y)  # Plot the Bessel function
plt.xlabel('$z$', fontsize=18)  # Use LaTeX syntax for x-axis label with fontsize 18
plt.ylabel('$J_0(z)$', fontsize=18)  # Use LaTeX syntax for y-axis label with fontsize 18
# plt.xlim(0, 20)  # Set the x-axis limits to 0 and 20
plt.grid(True)
# plt.show()

plt.savefig('bessel.pdf', dpi=200, bbox_inches='tight')
