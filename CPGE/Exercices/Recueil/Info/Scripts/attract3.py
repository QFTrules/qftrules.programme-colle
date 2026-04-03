def inverse(G):
    IG = {s:[] for s in G}  # initialisation de IG
    for s1 in G:            # boucle sur sommets s1 de G
        for s2 in G[s1]:    # boucle sur successeurs s2 de s1
            ...             # à compléter
    return IG               # renvoie inverse de G
