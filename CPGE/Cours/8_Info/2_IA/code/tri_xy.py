def tri(E, x, d):
    """
    Entrée : ensemble d’apprentissage E (list), point x (tuple),
             distance d (function)
    Action : tri l’ensemble E selon la distance des points à x
    Sortie : ensemble E trié (list)
    """
    return sorted(E, key = lambda y:d(x,y))
