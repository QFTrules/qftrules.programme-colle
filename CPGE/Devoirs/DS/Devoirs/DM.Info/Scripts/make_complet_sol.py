def make_complet(n):
    """
    Entrée : nombre de sommets n, de type int
    Sortie : graphe G, de type list[list[int]]
    """
    G = []
    for i in in range(n):
        G.append([])
        for j in range(n):
            if i!=j:
                G[i].append(j)
    return G
