def precision(M,N):
    """
    Entrée : M = matrice de confusion, N = nombre de prédictions
    Sortie : précision = Nc/N
    """
    n    = len(M)                       # nombre de classes
    diag = [M[i][i] for i in range(n)]  # diagonale = prédictions correctes
    Nc   = sum(diag)                    # nombre prédictions correctes
    return Nc/N                         # précision
