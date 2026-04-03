import numpy as np					# bibliothèque de calcul
import matplotlib.pyplot as plt		# bibliothèque de tracé

# PARAMÈTRES GRAPHIQUES
police = 25
plt.rcParams.update({'text.usetex':True,"font.family": "DejaVu Sans"})

# PARAMÈTRES PHYSIQUES
K = 0.5     # diffusivité thermique
L = 1.0     # taille du domaine
Time = 0.1  # temps total d’intégration

# PARAMÈTRES NUMERIQUES
NX = 100    # résolution spatiale
NT = 1000   # nombre de pas de temps

dx = L/(NX-1)  # pas spatial
dt = Time/NT   # pas de temps


### PROGRAMME ###

# Initialisation
x = np.linspace(0.0,1.0,NX)	# espace
T = np.sin(2*np.pi*x)		# température
dT = np.zeros((NX))			# variation (temporelle) de température

plt.figure()				# initialisation de la figure

# Boucle : méthode des différences finies
for n in range(0,NT):		# temps
	
	# Version naïve : boucle sur l’espace
	# for j in range (1, NX-1):
	#	 dT[j] = dt*K*(T[j-1]-2*T[j]+T[j+1])/(dx**2)	# dt*T’(t) = dt*kappa*d^2T/dx^2
	#	 T[j] += dT[j]									# T(t+dt) = T(t) + dt*T’(t)
		
	# Version rapide : instruction vectorielle
	dT[1:-1] = dt * K * (T[:-2] - 2 * T[1:-1] + T[2:]) / (dx**2)
	T += dT

# Trace tous les 100 pas de temps
	if (n%100 == 0):
		plotlabel = "t = %1.2f" %(n * dt)
		plt.plot(x, T, label=plotlabel, color = plt.get_cmap('copper')(float(NT-n)/NT))
	  
# Graphique
plt.xticks(fontsize=int(police*0.9))
plt.yticks(fontsize=int(police*0.9))
plt.xlabel(r'$x$', fontsize=police)
plt.ylabel(r'$T$', fontsize=police, rotation=0)
plt.title(r'Equation de la chaleur 1D',fontsize=police)
plt.legend()
plt.show()
