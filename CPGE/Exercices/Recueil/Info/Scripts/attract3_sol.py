def inverse(G):
    IG = {s: [] for s in G}
    for s1 in G:
        for s2 in G[s1]:
            IG[s2].append(s1)
    return IG
