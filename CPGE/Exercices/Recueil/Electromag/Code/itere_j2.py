def itere_J(V, rhos, frontiere):
    V1 = np.copy(V) # creation de la copie non modifiée à chaque itération
    N, M = V.shape # nombre de lignes et colonnes du tableau
    for i in range(N):
        for j in range(M):
            V[i, j] = nouveau_potentiel(V1, rhos, frontiere, i, j)
            # on modifie bien V mais pas V1 qui sert au calcul des éléments de V
    err = calcul_erreur(V1, V) # calcul de l'écart entre ancien et nouveau tableau
    return err