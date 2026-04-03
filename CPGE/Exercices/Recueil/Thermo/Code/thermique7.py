def calc_norme(vecteur):
    N = len(vecteur)             # taille du vecteur
    norme = 0                    # initialisation de la norme
    for i in range(N):           # boucle sur les éléments du vecteur
        norme += (vecteur[i])**2 # somme des carrés
    return norme**(0.5)          # racine carrée de la somme
