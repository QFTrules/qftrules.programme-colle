# Boucle sur le temps : méthode des différences finies
for n in range(0,NT):
	
	# Version naïve itérative : boucle sur l’espace
	for j in range (1, NX-1):
		 dT[j] = dt * K * (T[j-1]-2*T[j]+T[j+1]) / (dx**2)
		 T[j] += dT[j]									
		
	# Version rapide : instruction vectorielle
	dT[1:-1] = dt * K * (T[:-2] - 2 * T[1:-1] + T[2:]) / (dx**2)
	T       += dT

# Remarque : on pourraît même se passer de la variable auxiliaire dT
