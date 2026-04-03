def precision(M):
    """
    Calcule la précision de l'algorithme des k plus proches voisins sur la matrice de confusion M.
    """
    return sum(M[i][i] for i in range(3))/sum(sum(M[i]) for i in range(3))