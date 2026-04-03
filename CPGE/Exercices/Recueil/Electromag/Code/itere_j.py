def calcul_erreur(V1, V2): # calcule l'écart entre les deux tableaux V1 et V2
    N, M =V1.shape # récupère le nombre de lignes et colonnes du tableau
    E = 0 # initialisation de la somme définissant l'erreur
    for i in range(N): # boucle de parcours des lignes
        for j in range(M): # boucle de parcours des colonnes
            E = E + (V1[i, j] - V2[i, j]) ** 2 # calcul de la somme
    E = np.sqrt(E) / N # ne pas oublier de prendre la racine et de diviser par N
    return E