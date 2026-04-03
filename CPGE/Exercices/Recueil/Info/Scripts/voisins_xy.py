def voisins(E, x, d, k):
    """
    Entrée : E (list), x (tuple), d (func), k (int)
    Action : détermine les k plus proches voisins de x parmi les points de E
    Sortie : k plus proches voisins (list)
    """
    liste = tri(E, x, d) # liste triée (suivant distance d)
    ...                  # à compléter