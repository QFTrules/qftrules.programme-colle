import numpy as np

# Initialisation
x = np.linspace(0.0,1.0,NX)  # espace
T = np.sin(2*np.pi*x)        # température
dT = np.zeros((NX))          # variation de température
