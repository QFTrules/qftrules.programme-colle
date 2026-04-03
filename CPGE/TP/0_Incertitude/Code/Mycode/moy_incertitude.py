import numpy as np

# exemple de jeu de données
X = [5.2,4.9,5.0,4.8,5.1]
N = len(X)

# moyenne = valeur mesurée
moy_X =  np.mean(X)

# incertitude-type
sigma_X = np.std(X,
            ddof=1) # cette option choisit le coefficient N-1
Delta_X = sigma_X/np.sqrt(N)

# affichage du résultat de mesure
print("Résultat de mesure = %.1f +- %.1f"%(moy_X,Delta_X))
