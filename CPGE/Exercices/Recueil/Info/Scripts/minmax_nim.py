def minmax(G,s):
    """
    Entrée : graphe G (dictionnaire), sommet initial s
    Sortie : heuristique h(s) (entier)
    """
    if G[s] == []:
        if s[0] == 1:
            return ...
        else:
            return ...
    else:
        h = [minmax(G,v) for v in G[s]]
        if s[0] == 1:
            return ...
        else:
            return ...
