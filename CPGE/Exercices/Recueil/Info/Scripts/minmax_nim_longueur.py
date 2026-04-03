def parcours(G,s0):
    """
    Entrée : graphe G (dictionnaire), sommet initial s0 = (j,i)
    Sortie : None
    """
    atraiter = [s0]
    while len(atraiter) > 0:
        s = atraiter.pop()
        for v in G[s]:
            atraiter.append(v)
