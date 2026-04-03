def voisins(E, x, d, k):
    """
    Entrée : ensemble d’apprentissage E (list), point x (tuple),
             distance d (function), nombre plus proches voisins k (int)
    Action : détermine les k plus proches voisins de x parmi les points de E
    Sortie : k plus proches voisins (list)
    """
    liste = tri(E, x, d) # liste triée (suivant distance d)
    ...                  # à compléter