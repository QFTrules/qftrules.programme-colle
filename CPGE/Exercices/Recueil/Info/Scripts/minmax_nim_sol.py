def minmax(G,s):
    """
    Entrée : graphe G (dictionnaire), sommet initial s = (j,i)
    Sortie : heuristique h(s) (entier)
    """
    if G[s] == []:
        if s[0] == 1:
            return -1
        else:
            return +1
    else:
        h = [minmax(G,v) for v in G[s]]
        if s[0] == 1:
            return max(h)
        else:
            return min(h)
