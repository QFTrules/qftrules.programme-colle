def confusion(E, T, d, k, p, n):
    """
    Entrées : ensemble d'apprentissage E, ensemble de test T, distance d,
              nombre de voisins k, dictionnaire de classes p, nombre de classes n
    Sortie : matrice de confusion M
    """
    M = [[0]*n for l in range(n)]   # initialisation matrice
    for x in T:                     # boucle sur ensemble test
        i = p[x]                    # classe réelle
        j = classemaj(E,x,d,k,p)    # classe prédite
        M[i][j] += 1                # ajout au compte
    return M                        # retourne matrice de confusion
