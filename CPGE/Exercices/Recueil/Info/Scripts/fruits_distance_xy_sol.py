def distance(p1, p2):
    """
    Entrée : p1 (tuple) : point du plan de coordonnées (masse, couleur)
            p2 (tuple) : point du plan de coordonnées (masse, couleur)
    Sortie : d (float) : distance euclidienne pondérée entre p1 et p2
    """
    m1, c1 = p1
    m2, c2 = p2
    d = ((m1/300 - m2/300)**2 + (c1 - c2)**2)**0.5
    return d