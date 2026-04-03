def confusion(E, T, d, k, p, n):
    """
    Entrées : E (list), T (list), d (func), k (int), p (dict), n (int)
    Sortie : matrice de confusion M
    """
    M = [[0]*n for l in range(n)]           # initialisation matrice
    for x in T:                             # boucle sur ensemble test
        i = numero[p[x]]                    # classe réelle
        j = numero[classemaj(E,x,d,k,p)]    # classe prédite
        M[i][j] += 1                        # ajout au compte
    return M                                # retourne matrice de confusion
