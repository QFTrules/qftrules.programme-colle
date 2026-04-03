def classe(E, x, d, k, p):
    """
    Entrée : ensemble d’apprentissage E (list), point x (tuple),
             distance d (function), nombre plus proches voisins k (int),
             classification p (dict)
    Action : détermine la classe majoritaire de x parmi les k plus proches voisins
    Sortie : classe majoritaire (int)
    """
    v = voisins(E, x, d, k)             # k plus proches voisins de x
    c = {p[y]:0 for y in v}             # liste des classes des voisins
    for y in v:                         # boucle sur voisins
        c[p[y]] += 1                    # comptage des classes
    maxi = 0                            # initialisation maximum
    for i in c:                         # boucle sur classes des voisins
        if c[i] > maxi:                 # si classe i plus nombreuse
            maxi, classmaj = c[i], i    # mise à jour classe majoritaire
    return classmaj                     # retourne classe majoritaire
