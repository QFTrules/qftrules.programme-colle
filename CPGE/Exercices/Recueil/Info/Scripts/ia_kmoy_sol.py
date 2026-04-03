def kmoy(k, E, d, n):
    """
    Entrée : k (int) : nombre de classes
              E (list) : ensemble de données
              d (func) : une distance
              n (int) : nombre d'itérations
    Renvoie la classification des données E obtenue par l'algorithme des k-moyennes.
    Sortie : p (dict) : la classification des données E
    """
    centres = init_centres(k, E)
    for j in range(n):
        p = partition(E, centres, d)
        i = 0
        for classe in p.values():
            centres[i] = barycentre([x for x in p if p[x] == classe])
            i += 1
    return p