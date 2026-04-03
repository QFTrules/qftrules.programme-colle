def est_complet(G, n):
    """
    Entrée : nombre de sommets n, de type int ; graphe G, de type list[list[int]]
    Sortie : True ou False, de type bool
    """
    if len(G) != n:
        return False
    for L in G:
        if len(L) != n-1:
            return False
    return True    
