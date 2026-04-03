def classemaj(E, x, d, k, p):
    """
    Entrée : E (list), x (tuple), d (func), k (int), p (dict)
    Action : détermine la classe majoritaire de x parmi les k plus proches voisins
    Sortie : classe majoritaire (int)
    """
    v = voisins(E, x, d, k)
    c = {p[y]:0 for y in v}
    for y in v:
        c[p[y]] += 1
    maxi = 0
    for i in c:
        if c[i] > maxi:
            maxi, classmaj = c[i], i
    return classmaj
